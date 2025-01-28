import { CheerioAPI, load as loadDom } from "cheerio";
import { writeFile } from "node:fs/promises";

export interface ContestInfo {
	years: YearDetails[];
	events: EventDetails[];
}

interface YearDetails {
	year: number;
	place: number;
	points: number;
	countryPlace: number;
}

async function loadTeamPage(): Promise<ContestInfo> {
	const res = await fetch("https://ctftime.org/team/177350");
	const data = await res.text();
	const dom = loadDom(data);

	// Hook onto #rating_2022
	const el = dom("p:contains(Overall rating place)");
	const el2 = el.next();
	const text = `${el.text()} ${el2.text()}`;
	const pat =
		/Overall rating place:\s+(\d+)\s+with (\d+(?:\.\d+)?) pts in (\d+)\s+Country place:\s+(\d+)/;
	const m = pat.exec(text);
	const years: YearDetails[] = [];
	if (m !== null) {
		const [_, place, points, year, countryPlace] = [...pat.exec(text)];
		years.push({
			place: Number.parseInt(place),
			points: Number.parseFloat(points),
			year: Number.parseInt(year),
			countryPlace: Number.parseInt(countryPlace),
		});
	}

	const events: EventDetails[] = [];
	const placeIcos = dom("td.place_ico");
	// return await Promise.all(placeIcos.map((i, el) => handleCtfEvent(dom, el)));
	for (const el of placeIcos) {
		events.push(await handleCtfEvent(dom, el));
	}
	return { years, events };
}

async function handleCtfEvent(
	dom: CheerioAPI,
	el: Element,
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
	return {
		id: `ctftime-${id}`,
		place,
		name,
		link,
		points,
		ratingPoints,
		start,
		end,
	};
}

export interface EventPageDetails {
	start?: Date;
	end?: Date;
}

export interface EventDetails extends EventPageDetails {
	id: string;
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
	JSON.stringify(events, null, 2),
);
