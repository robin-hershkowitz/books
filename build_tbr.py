#!/usr/bin/env python3
"""Build tbr.html from the book data below. Same structure as build_fivestar.py:
data first, markup generated. Edit BOOKS, then re-run."""

import html
import re

# title, author, year, tags, description
BOOKS = [
    ("Never Whistle at Night, Part II: Back for Blood", "ed. Shane Hawk &amp; Theodore C. Van Alst Jr.", 2026,
     ["horror", "short stories"],
     "The bestselling Indigenous dark fiction anthology returns with a second round of stories, this time leaning harder into monsters and mutilation. New contributors join returning ones, and the range runs from folkloric dread to outright body horror."),

    ("Big Swiss", "Jen Beagin", 2023,
     ["literary", "contemporary", "humor"],
     "Greta transcribes sessions for a sex coach in Hudson, New York, and becomes obsessed with a client she nicknames Big Swiss. When she recognizes the voice at the dog park, she introduces herself under a false name and lets the affair run on a lie. Filthy, very funny, and sharper about trauma than its premise suggests."),

    ("I Found a Lost Hallway in a Dying Mall", "Ben Farthing", 2024,
     ["horror"],
     "Lisa finds her elderly coworker in an abandoned wing of a failing mall, talking to a circle of mannequins whose limbs are fused at wrong angles. When she looks away, they move, and the hallway is longer than it was. Liminal-space horror in the vein of creepypasta and SCP entries, and a standalone in the I Found series."),

    ("The Ending Writes Itself", "Evelyn Clarke", 2026,
     ["mystery", "thriller"],
     "Six struggling writers are invited to a private Scottish island by a reclusive bestselling novelist, only to learn on arrival that he is dead and his final book is unfinished. Whoever writes a worthy ending in seventy-two hours gets the career of a lifetime. A locked-room mystery and a publishing-industry satire, written by V. E. Schwab and Cat Clarke under a shared pen name."),

    ("Saint Sebastian's Abyss", "Mark Haber", 2022,
     ["literary", "humor"],
     "Two art critics build entire careers on a single sixteenth-century painting, then destroy their friendship over three words. One is dying and has summoned the other to Berlin after decades of silence. A short, spiraling comedy about obsession and scholarly vanity."),

    ("The Shutouts", "Gabrielle Korn", 2024,
     ["science fiction", "dystopian", "lgbtqia+"],
     "A companion to Yours for the Taking, following the people left outside the sealed climate havens rather than the ones let in. Letters from a mother to the daughter she abandoned braid together with a journey across a wrecked continent."),

    ("Death on the Lanai", "Rachel Ekstrom Courage", 2026,
     ["mystery", "humor"],
     "The Golden Girls accept a mysterious invitation to a party on a private Biscayne Bay island, delivered with a jewel-encrusted brooch and a promise to honor the greatest artist of the century. Then someone turns up dead. Second in the licensed cozy series that began with Murder by Cheesecake."),

    ("Game On", "Navessa Allen", 2026,
     ["romance", "contemporary"],
     "Tyler Neumann wants to destroy the father he has never met, and blackmailing tattoo artist Stella McCormick into playing his girlfriend is how he plans to get inside her family's circles. Loathing at first sight curdles into something else. Book three of the Into Darkness series, enemies to lovers, extremely spicy, with a content warning up front."),

    ("Scarred: A Memoir of a Childhood Stolen and a Life Reclaimed", "Clark Fredericks", 2025,
     ["memoir", "nonfiction", "true crime"],
     "Fredericks was groomed and abused for years by his small-town New Jersey Scout leader, a man everyone else regarded as a local hero. He stayed silent into adulthood, numbing it with addiction, until the night he killed his abuser and stood trial for murder. A hard read about trauma, vengeance, and what came after."),

    ("Little Movements", "Lauren Morrow", 2025,
     ["literary", "contemporary"],
     "Layla Smart leaves her husband and her Brooklyn life for a prestigious choreography residency at Briar House, an arts institution in rural Vermont. She wants to make art for its own sake; the director wants her to mine her people's history. Then the institution's own history surfaces, along with a betrayal at home and a pregnancy. Darkly funny debut."),

    ("Where the Girls Were", "Kate Schatz", 2026,
     ["historical", "feminism"],
     "San Francisco, 1968. Baker is a valedictorian and a good girl until one night at the Fillmore, and the pregnancy that follows sends her to a home for unwed mothers. Inside a Victorian full of girls hiding the same secret, she finds shame, no choices at all, and unexpected solidarity."),

    ("The White Road", "Sarah Lotz", 2017,
     ["horror", "thriller"],
     "A thrill-seeking blogger goes caving for footage of dead bodies, then talks his way onto an Everest expedition for more. The mountain does not cooperate. Survival horror that gets colder and stranger the higher it climbs."),

    ("The Red Tree", "Caitlin R. Kiernan", 2009,
     ["horror", "literary", "lgbtqia+"],
     "A novelist rents an isolated Rhode Island farmhouse to escape a breakup and finds the unfinished manuscript of the previous tenant, an anthropologist obsessed with the enormous oak on the property. Told as her own increasingly unreliable journal. Quiet, folkloric, and deeply unwell."),

    ("The Grip of It", "Jac Jemc", 2017,
     ["horror", "literary"],
     "Julie and James buy a cheap house in a small town to escape his gambling, and the house starts working on them. Stains bloom, rooms shift, bruises appear on her skin that no one can account for. A haunted-house novel that reads like a marriage falling apart from the inside."),

    ("King Sorrow", "Joe Hill", 2025,
     ["horror", "fantasy"],
     "Cornered into stealing rare books from his college library, Arthur Oakes lets his friends summon a dragon out of a journal bound in human skin. It solves his problem. Then it wants a fresh sacrifice every year, forever. Hill's first novel in nine years, and about nine hundred pages of dark academia turning into epic horror."),

    ("Primates of Park Avenue", "Wednesday Martin", 2015,
     ["memoir", "nonfiction", "sociology"],
     "An anthropologist by training moves to the Upper East Side and studies the mothers there as a field site: the hierarchies, the handbags as status displays, the ritualized exclusion. Read as ethnography or as gossip; it works either way."),

    ("Same As It Ever Was", "Claire Lombardo", 2024,
     ["literary", "contemporary"],
     "Julia Ames has finally settled into a stable midlife when a chance encounter with a woman from her past reopens everything she buried. Moves between her chaotic upbringing and the marriage and motherhood she has been quietly failing at. Long, interior, and very good on how a person keeps not becoming who they meant to be."),

    ("The Archive Undying", "Emma Mieko Candon", 2023,
     ["science fiction", "lgbtqia+"],
     "When an AI god goes mad and dies, everything it touched is corrupted, and Sunai walks out of the wreckage unable to die. He spends decades drinking and running from what he is until he takes a job on a salvage crew that knows exactly what he is worth. Dense, strange mecha science fiction that refuses to explain itself upfront."),

    ("Kushiel's Dart", "Jacqueline Carey", 2001,
     ["fantasy", "romance"],
     "Phedre no Delaunay is born with a scarlet mote in her eye, marking her as chosen to find pleasure in pain, and is trained as both courtesan and spy in a kingdom descended from angels. What she overhears in bed turns out to be treason. Doorstop-sized political fantasy with a distinctive erotic engine."),

    ("Far from the Light of Heaven", "Tade Thompson", 2021,
     ["science fiction", "mystery"],
     "Michelle Campion's first command should have been uneventful: a colony ship on autopilot, a thousand sleeping passengers. She wakes to find dozens of them murdered and dismembered, and the ship's AI unable to say how. A locked-room mystery in deep space."),

    ("Mary: An Awakening of Terror", "Nat Cassidy", 2022,
     ["horror"],
     "Mary is fifty-something, invisible, quietly falling apart, and newly unemployed when she returns to the Arizona town where she grew up to settle her aunt's affairs. Menopause, hallucinations, and a very old local horror arrive together. Nasty, funny, and unusually tender toward its protagonist."),

    ("Notes on Infinity", "Austin Taylor", 2025,
     ["literary", "contemporary", "technology"],
     "Two Harvard chemistry students fall for each other while chasing an anti-aging breakthrough, drop out to found a biotech company, and become famous fast. What holds up under a funding round does not hold up under scrutiny. A campus romance that turns into a fraud story."),

    ("The Postmortal", "Drew Magary", 2011,
     ["science fiction", "dystopian"],
     "A cure for aging is discovered and quietly distributed, and nobody stops to ask what happens to a planet where no one dies of old age. Told as the digital record of one man who takes the cure at twenty-nine and lives through the consequences. Satirical, then genuinely bleak."),

    ("The Golden Mean", "Annabel Lyon", 2009,
     ["historical", "literary"],
     "Aristotle, stranded in the Macedonian court and prone to what he would not have called depression, is assigned to tutor a boy who will become Alexander the Great. A portrait of a difficult, brilliant teacher and a student he cannot make virtuous. Spare, physical prose."),

    ("Cry to Heaven", "Anne Rice", 1982,
     ["historical", "literary"],
     "A Venetian nobleman's son is castrated and sent to a Naples conservatory, where he trains as a castrato alongside a Sicilian boy who has already lost everything to the same knife. Opera, revenge, and eighteenth-century Italy rendered at full Rice intensity."),

    ("Hell's Heart", "Alexis Hall", 2026,
     ["science fiction", "lgbtqia+"],
     "Earth is dead and humanity runs on fluid harvested from leviathans that swim the atmosphere of Jupiter. A nameless narrator signs onto the Pequod for money, follows a captain called A into her obsession, and falls for a woman from old Earth who speaks mostly in Latin. Moby-Dick retold as a queer, filthy, very funny space opera."),

    ("The Hike", "Drew Magary", 2016,
     ["fantasy", "horror"],
     "Ben steps out of a Pennsylvania hotel for a quick walk before a business meeting and cannot get back. The path will not let him leave, and what he meets on it includes a talking crab, a giantess, and men wearing dog faces. Fairy-tale logic with the cruelty left in."),

    ("The Wall", "Marlen Haushofer, trans. Shaun Whiteside", 1963,
     ["literary", "speculative fiction", "classics"],
     "A woman wakes in an Austrian hunting lodge to find an invisible wall sealing her off from a world where everything beyond it appears to have died mid-motion. What follows is the record of her survival with a dog, a cow, and a cat. Less a disaster novel than a long, austere meditation on solitude and care."),

    ("A Libertarian Walks Into a Bear", "Matthew Hongoltz-Hetling", 2020,
     ["nonfiction", "humor", "sociology"],
     "In 2004 a group of libertarians moved en masse to Grafton, New Hampshire, to build a town free of government. Services collapsed, trash accumulated, and the bears got bold. Reported with a straight face, which makes it funnier."),

    ("Bog Queen", "Anna North", 2025,
     ["historical", "mystery"],
     "An American forensic anthropologist is called to post-Brexit England to identify a perfectly preserved body pulled from a peat bog. The second thread belongs to the Iron Age druid whose body it is, and the moss itself gets a few pages. Peat-cutters want to sell the bog; activists want it untouched."),

    ("What a Time to Be Alive", "Jade Chang", 2025,
     ["literary", "contemporary", "humor"],
     "Lola Treasure Gold is grieving her best friend and broke in Los Angeles when a video of her goes viral and turns her into an accidental wellness guru. She is either a scammer or a sage and cannot tell which. Satirical about the belief economy without being cruel to the woman selling it."),

    ("Pan", "Michael Clune", 2025,
     ["literary", "contemporary"],
     "A fifteen-year-old in suburban Illinois starts having panic attacks and concludes, not unreasonably given the evidence, that the god Pan has entered him. He and his friends build a theology around it. A debut novel about adolescent dread that takes the metaphysics seriously."),

    ("Sleeping Giants", "Sylvain Neuvel", 2016,
     ["science fiction", "thriller"],
     "A girl falls into a hole in South Dakota and lands in the palm of a giant metal hand. Seventeen years later she leads the team assembling the rest of the body from pieces buried around the world. Told entirely in interviews, logs, and transcripts."),

    ("Lone Women", "Victor LaValle", 2023,
     ["horror", "historical", "western"],
     "Adelaide Henry burns down her family's California farm and heads to Montana in 1915 to homestead alone, carrying an enormously heavy steamer trunk she never opens in front of anyone. Frontier historical fiction with something monstrous locked inside it, and a real interest in the Black and immigrant women who actually settled that land."),

    ("Albion", "Anna Hope", 2025,
     ["literary", "contemporary"],
     "The Brooke family gathers over five days at their thousand-acre Sussex estate to bury a charismatic, ruinous patriarch. One daughter wants to rewild it, her brother wants a psychedelic retreat for the very rich, and a woman arrives from America with a truth that will take the whole thing apart. Succession by way of the English country house novel."),

    ("Bad Manners", "Amy Beashel", 2026,
     ["thriller", "feminism", "contemporary"],
     "A men-only charity dinner, a group of young waitresses, jokes that stop being jokes, and hands that linger. What happens that night ripples out through families and years. A furious novel about male violence and about the women who were taught it would be rude to make a scene."),

    ("Coup de Gr\u00e2ce", "Sofia Ajram", 2024,
     ["horror", "lgbtqia+"],
     "A young man on his way to end his life gets off at a Montreal metro station and cannot find the exit. Escalators lead to more escalators, tiled corridors loop, and the station keeps unfolding. Liminal horror that is really about wanting to stop."),

    ("Monstrilio", "Gerardo S\u00e1mano C\u00f3rdova", 2023,
     ["horror", "literary", "lgbtqia+"],
     "After her eleven-year-old son dies, Magos cuts out a piece of his lung and keeps it. It grows. It eats. It starts to resemble the boy. Told in four voices across years, a novel about grief that refuses to let the monster be only a metaphor."),

    ("Salvage the Bones", "Jesmyn Ward", 2011,
     ["literary", "contemporary"],
     "Twelve days in rural Mississippi as Hurricane Katrina approaches, narrated by fifteen-year-old Esch, who is pregnant and reading Greek myth while her brother fights his pit bull for money. Fierce, physical, National Book Award winner."),

    ("The Book of Luke", "Lovell Holder", 2025,
     ["contemporary", "lgbtqia+", "humor"],
     "Ten years after winning a brutal reality competition show, Luke Griffin's marriage to the first openly gay senator implodes, and he goes back on the show that made him. Dual timelines, cliffhangers, and a real interest in what fame does to a person over a decade."),

    ("Woodworking", "Emily St. James", 2025,
     ["literary", "contemporary", "lgbtqia+"],
     "Erica, a high school teacher in small-town South Dakota in 2016, comes out to exactly one person: a trans teenager at her school who has no interest in being anyone's mentor. Funny and specific about transition, the Great Plains, and an election closing in."),

    ("What Is Queer Food?", "John Birdsall", 2025,
     ["nonfiction", "history", "lgbtqia+"],
     "A history of twentieth-century queer American life told through kitchens, dinner parties, and cookbooks, from James Beard and Alice B. Toklas onward. Argues that queer food is less a cuisine than a set of survival strategies."),

    ("The Hounding", "Xenobe Purvis", 2025,
     ["historical", "literary"],
     "In a drought-stricken eighteenth-century English village, five sisters are said by their neighbors to turn into dogs. The novel is less interested in whether it is true than in how quickly a community decides to act on it. Short, dry, and menacing."),

    ("A Marriage at Sea", "Sophie Elmhirst", 2025,
     ["nonfiction", "history"],
     "In 1973 Maurice and Maralyn Bailey sold everything to sail to New Zealand, and a whale sank their boat in the Pacific. They survived one hundred and eighteen days in a raft. A portrait of a marriage stripped to its structure."),

    ("Heart the Lover", "Lily King", 2025,
     ["literary", "romance"],
     "A writer looks back on the two men she loved at once in college, the books that passed between them, and the decades that followed. Short, exact, and mostly about how a first love keeps rearranging the rest of a life."),
]

GENRE_HEX = [
    "#e0b04c", "#d4707e", "#6fae8f", "#7d9bd1", "#c98f5e",
    "#9d84c9", "#5eb3b8", "#c96a4e", "#b8c95e",
]

CSS_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>To Be Read</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #16151a;
    --card: #1f1e25;
    --text: #eceae4;
    --muted: #a49f93;
    --star: #e0b04c;
    --g-decade: #9aa0a8;
%(genre_vars)s  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    line-height: 1.55;
    padding: 2.5rem 1.25rem 4rem;
  }

  header { max-width: 1100px; margin: 0 auto 1.6rem; }

  .nav {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    margin-bottom: 1.1rem;
  }

  .nav:hover, .nav:focus-visible { color: var(--text); border-bottom-color: var(--muted); outline: none; }

  h1 {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: clamp(2rem, 5vw, 3rem);
    letter-spacing: 0.01em;
  }

  .subtitle { color: var(--muted); margin-top: 0.4rem; font-size: 0.95rem; }

  .filters {
    max-width: 1100px;
    margin: 0 auto 2rem;
    padding-top: 1.3rem;
    border-top: 1px solid rgba(255,255,255,0.08);
  }

  .filters-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
  }

  .chip-row { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }

  .status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.04em;
    color: var(--muted);
    margin-top: 0.85rem;
  }

  .clear {
    font-family: 'Inter', sans-serif;
    font-size: 0.74rem;
    font-weight: 600;
    color: var(--star);
    background: none;
    border: none;
    padding: 0;
    margin-left: 0.6rem;
    cursor: pointer;
    text-decoration: underline;
  }

  .clear[hidden] { display: none; }

  .tag {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    color: var(--tc, var(--muted));
    background: color-mix(in srgb, var(--tc, var(--muted)) 15%%, transparent);
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 0.15rem 0.45rem;
    white-space: nowrap;
    cursor: pointer;
    transition: border-color 0.14s ease, background 0.14s ease;
  }

  .tag:hover, .tag:focus-visible { border-color: var(--tc, var(--muted)); outline: none; }

  .tag[aria-pressed="true"] {
    background: var(--tc, var(--muted));
    color: var(--bg);
    border-color: var(--tc, var(--muted));
  }

  .decade { font-family: 'IBM Plex Mono', monospace; --tc: var(--g-decade); }

  .year {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    color: var(--text);
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    padding: 0.15rem 0.45rem;
  }

%(genre_classes)s
  .shelf { max-width: 1100px; margin: 0 auto; columns: 3 300px; column-gap: 1.1rem; }

  .book {
    background: var(--card);
    border-left: 3px solid var(--star);
    border-radius: 6px;
    padding: 1.1rem 1.15rem 1.2rem;
    margin-bottom: 1.1rem;
    break-inside: avoid;
  }

  .book[hidden] { display: none; }

  .book h2 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.12rem; line-height: 1.25; }

  .author { color: var(--muted); font-size: 0.85rem; margin: 0.25rem 0 0.4rem; }

  .tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.6rem; }

  .more {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--star);
    background: none;
    border: none;
    border-bottom: 1px solid rgba(224,176,76,0.4);
    padding: 0;
    margin-top: 0.7rem;
    cursor: pointer;
  }

  .more:hover, .more:focus-visible { border-bottom-color: var(--star); outline: none; }

  .desc-source { display: none; }

  .empty { max-width: 1100px; margin: 0 auto; color: var(--muted); font-size: 0.95rem; }
  .empty[hidden] { display: none; }

  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(10,9,13,0.78);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    z-index: 50;
  }

  .overlay[hidden] { display: none; }

  .modal {
    background: var(--card);
    border-left: 4px solid var(--star);
    border-radius: 8px;
    max-width: 560px;
    width: 100%%;
    max-height: 85vh;
    overflow-y: auto;
    padding: 1.8rem 1.9rem 2rem;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6);
  }

  .modal h3 { font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.5rem; line-height: 1.2; }

  .modal-author { color: var(--muted); font-size: 0.9rem; margin: 0.3rem 0 0.45rem; }

  .modal-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    color: var(--muted);
  }

  .modal-desc { font-size: 0.95rem; margin-top: 1.3rem; }

  .modal-close {
    display: block;
    margin: 1.5rem 0 0 auto;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--star);
    background: none;
    border: 1.5px solid var(--star);
    border-radius: 5px;
    padding: 0.4rem 0.9rem;
    cursor: pointer;
  }

  .modal-close:hover, .modal-close:focus-visible { background: var(--star); color: var(--bg); outline: none; }

  @media (prefers-reduced-motion: reduce) { .tag { transition: none; } }
</style>
</head>
<body>
"""

JS = """<script>
  (function () {
    var shelf = document.getElementById('shelf');
    var books = Array.prototype.slice.call(shelf.querySelectorAll('.book'));
    var legendChips = Array.prototype.slice.call(document.querySelectorAll('#legend .tag'));
    var countEl = document.getElementById('count');
    var clearEl = document.getElementById('clear');
    var emptyEl = document.getElementById('empty');
    var overlay = document.getElementById('overlay');
    var mTitle = document.getElementById('m-title');
    var mAuthor = document.getElementById('m-author');
    var mMeta = document.getElementById('m-meta');
    var mDesc = document.getElementById('m-desc');
    var mClose = document.getElementById('m-close');
    var active = [];
    var lastFocus = null;

    function apply() {
      var shown = 0;
      books.forEach(function (book) {
        var tags = (book.getAttribute('data-tags') || '').split('|');
        var match = active.every(function (f) { return tags.indexOf(f) !== -1; });
        book.hidden = !match;
        if (match) shown++;
      });
      countEl.textContent = shown;
      clearEl.hidden = active.length === 0;
      emptyEl.hidden = shown !== 0;
      legendChips.forEach(function (chip) {
        var on = active.indexOf(chip.getAttribute('data-filter')) !== -1;
        chip.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    }

    function openModal(book) {
      var desc = book.querySelector('.desc-source');
      mTitle.textContent = book.querySelector('h2').textContent;
      mAuthor.textContent = book.querySelector('.author').textContent;
      mMeta.textContent = book.getAttribute('data-meta') || '';
      mDesc.textContent = desc ? desc.textContent.trim() : '';
      lastFocus = document.activeElement;
      overlay.hidden = false;
      mClose.focus();
    }

    function closeModal() {
      overlay.hidden = true;
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    document.addEventListener('click', function (e) {
      var target = e.target;
      if (target === mClose || target === overlay) { closeModal(); return; }
      if (target.id === 'clear') { active = []; apply(); return; }
      if (target.classList && target.classList.contains('more')) {
        var card = target.closest('.book');
        if (card) openModal(card);
        return;
      }
      if (target.classList && target.classList.contains('tag')) {
        var value = target.getAttribute('data-filter');
        if (!value) return;
        var i = active.indexOf(value);
        if (i === -1) { active.push(value); } else { active.splice(i, 1); }
        apply();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !overlay.hidden) closeModal();
    });

    apply();
  })();
</script>
"""


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.replace('+', 'plus').lower()).strip('-')


def decade(year):
    return str(year - year % 10) + 's'


def main():
    genres = sorted({g for b in BOOKS for g in b[3]})
    decades = sorted({decade(b[2]) for b in BOOKS})

    genre_vars = ''.join(
        "    --g-%s: %s;\n" % (slug(g), GENRE_HEX[i % len(GENRE_HEX)])
        for i, g in enumerate(genres)
    )
    genre_classes = ''.join(
        "  .g-%s { --tc: var(--g-%s); }\n" % (slug(g), slug(g)) for g in genres
    )

    out = [CSS_HEAD % {'genre_vars': genre_vars, 'genre_classes': genre_classes}]

    out.append("""
<header>
  <a class="nav" href="./index.html">&larr; All shelves</a>
  <h1>To Be Read</h1>
  <p class="subtitle">%d books &middot; tap Description for more</p>
</header>

<section class="filters">
  <p class="filters-label">Filter &mdash; tap to combine</p>
  <div class="chip-row" id="legend">
""" % len(BOOKS))

    for d in decades:
        out.append('    <button class="tag decade" data-filter="%s" aria-pressed="false">%s</button>\n' % (d, d))
    for g in genres:
        out.append('    <button class="tag g-%s" data-filter="%s" aria-pressed="false">%s</button>\n'
                   % (slug(g), g, g))

    out.append("""  </div>
  <p class="status"><span id="count">%d</span> shown<button class="clear" id="clear" hidden>clear</button></p>
</section>

<main class="shelf" id="shelf">
""" % len(BOOKS))

    for title, author, year, tags, desc in BOOKS:
        data_tags = '|'.join([decade(year)] + tags)
        chips = ['<span class="year">%d</span>' % year,
                 '<button class="tag decade" data-filter="%s">%s</button>' % (decade(year), decade(year))]
        for g in tags:
            chips.append('<button class="tag g-%s" data-filter="%s">%s</button>' % (slug(g), g, g))
        out.append("""
  <article class="book" data-tags="%s" data-meta="%d">
    <div>
      <h2>%s</h2>
      <p class="author">%s</p>
      <div class="tags">%s</div>
      <button class="more">Description</button>
      <div class="desc-source">%s</div>
    </div>
  </article>
""" % (data_tags, year, html.escape(title), author, ''.join(chips), html.escape(desc)))

    out.append("""
</main>

<p class="empty" id="empty" hidden>No books match those filters.</p>

<div class="overlay" id="overlay" hidden>
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="m-title">
    <h3 id="m-title"></h3>
    <p class="modal-author" id="m-author"></p>
    <p class="modal-meta" id="m-meta"></p>
    <p class="modal-desc" id="m-desc"></p>
    <button class="modal-close" id="m-close">Close</button>
  </div>
</div>

""")
    out.append(JS)
    out.append("\n</body>\n</html>\n")

    with open('tbr.html', 'w', encoding='utf-8') as f:
        f.write(''.join(out))
    print('wrote tbr.html with %d books, %d genres' % (len(BOOKS), len(genres)))


if __name__ == '__main__':
    main()
