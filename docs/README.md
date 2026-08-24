# DataFrame of Mind: the slide deck

The course slides, written in [Slidev](https://sli.dev) with the Dataminded theme.
Converted from `DataFrame-of-Mind-with-Polars-and-PySpark.pptx`: one uniform theme across the
Polars and PySpark halves, and every code screenshot replaced by a real, syntax-highlighted
code block.

## Layout

| Path                     | What it is                                                |
| ------------------------ | --------------------------------------------------------- |
| `slides.md`              | The deck. Speaker notes live in the HTML comments.        |
| `style.css`              | Global CSS: the bit-block diagram, plus one Slidev workaround.     |
| `components/`            | Deck-local Vue components (timeline, trade-off triangle).          |
| `theme/`                 | The `slidev-theme-dataminded` sources, linked from `package.json`. |
| `public/img/`            | Diagrams and photos carried over from the original deck.  |
| `DataFrame-of-Mind.pdf`  | Latest export.                                            |

## Working on the deck

```bash
cd docs
npm install        # once
npm run dev        # live preview on localhost:3030, press "p" for presenter mode
npm run export     # writes DataFrame-of-Mind.pdf next to slides.md
npm run build      # static site in dist/
```

## Conventions

- Headings are two-tone: wrap the accent word in `<span class="dm-accent">...</span>`.
- Content slides use `layout: default` with a `label:` for the top-right tag. The label is the
  section name (`3 · Expressing a query`) and stays constant between section dividers, so every
  slide says where it is. Six sections, matching the agenda one for one.
- Dividers use `layout: section`, exercise and demo pointers use `layout: statement`.
- Components (`DmColumns`, `DmComparison`, `DmSteps`, `DmProcess`, `DmIconBadge`) come from the
  theme. The reference deck lives in
  [datamindedbe/playground-agentic-slides](https://github.com/datamindedbe/playground-agentic-slides).
- No emdashes, and bold marks a single term rather than a whole claim.
- Progressive builds from the original deck are single slides with `v-click` reveals. Slidev
  supports ranges (`v-click="[1, 3]"`), but note that `slidev export` flattens clicks to their
  final state, so keep the last state complete: anything that only exists mid-build is lost on
  paper.
- `style.css` is loaded once at startup. After editing it, restart the dev server; hot reload
  does not pick it up.
- Slides render at 980x552 CSS pixels. Anything taller silently overflows the page in the PDF
  export, so check the export after adding a long code block.
