import { CheerioAPI, load as loadDom } from "cheerio";
import * as ical from "cal-parser";
import { writeFile } from "node:fs/promises";

async function loadTeamPage(): Promise<EventDetails[]> {
  const res = await fetch("https://ctftime.org/team/177350");
  const data = await res.text();
  const dom = loadDom(data);

  const placeIcos = dom("td.place_ico");
  // return await Promise.all(placeIcos.map((i, el) => handleCtfEvent(dom, el)));
  const result = [];
  for (const el of placeIcos) {
    result.push(await handleCtfEvent(dom, el));
  }
  return result;
}

async function handleCtfEvent(
  dom: CheerioAPI,
  el: Element
): Promise<EventDetails> {
  const placeEl = dom(el).next();
  const place = Number.parseInt(placeEl.text());
  const ctfEl = placeEl.next();
  const linkEl = ctfEl.find("a");
  const name = linkEl.text();
  const linkPart = linkEl.attr("href") ?? "";
  const link = "https://ctftime.org" + linkPart;
  const matches = /\/event\/(\d+)/.exec(linkPart);
  const id = Number.parseInt(matches?.[1]!);
  const pointsEl = ctfEl.next();
  const points = Number.parseFloat(pointsEl.text());
  const ratingPointsEl = pointsEl.next();
  const ratingPoints = Number.parseFloat(ratingPointsEl.text());

  const { start, end } = await loadEventPage(id);
  return { place, name, link, points, ratingPoints, start, end };
}

interface EventPageDetails {
  start?: Date;
  end?: Date;
}

interface EventDetails extends EventPageDetails {
  name: string;
  place: number;
  points: number;
  ratingPoints: number;
  link: string;
}

async function loadEventPage(id: number): Promise<EventPageDetails> {
  const link = `https://ctftime.org/api/v1/events/${id}/`;
  console.log(link);
  const res = await fetch(link);
  let rawData = await res.text();
  // console.log(rawData);
  rawData = rawData.replace("\r", "\\r");
  rawData = rawData.replace("\n", "\\n");
  const data = JSON.parse(rawData);
  const startN = Date.parse(data.start);
  const endN = Date.parse(data.finish);
  const start = new Date(startN);
  const end = new Date(endN);
  return { start, end };
}

const events = await loadTeamPage();
await writeFile(
  "src/content/pages/contests.json",
  JSON.stringify(events, null, 2)
);
