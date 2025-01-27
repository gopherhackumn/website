import { CheerioAPI, load as loadDom } from "cheerio";
import * as ical from "cal-parser";
import { writeFile } from "node:fs/promises";

async function loadTeamPage(): Promise<EventDetails[]> {
  const res = await fetch("https://ctftime.org/team/177350");
  const data = await res.text();
  const dom = loadDom(data);

  const placeIcos = dom("td.place_ico");
  return await Promise.all(placeIcos.map((i, el) => handleCtfEvent(dom, el)));
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
  const link = "https://ctftime.org" + linkEl.attr("href");
  const pointsEl = ctfEl.next();
  const points = Number.parseFloat(pointsEl.text());
  const ratingPointsEl = pointsEl.next();
  const ratingPoints = Number.parseFloat(ratingPointsEl.text());

  const { start, end } = await loadEventPage(link);
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

async function loadEventPage(link: string): Promise<EventPageDetails> {
  const res = await fetch(link + ".ics");
  const data = await res.text();
  const calData = ical.parseString(data);
  const event = calData.events[0];
  const start = event?.dtstart?.value;
  const end = event?.dtend?.value;
  return { start, end };
}

const events = await loadTeamPage();
await writeFile("contests.json", JSON.stringify(events, null, 2));
