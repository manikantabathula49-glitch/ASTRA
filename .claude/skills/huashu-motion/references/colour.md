# Colour

Colour is the first thing a viewer judges and the quickest way for a film to look like every other
AI-made film. Product designers at the top of the field do not pick colours. They find them, then
build a system around them: a few roles, fixed proportions, and a reason for every hue.

Without a method an agent falls back on its own default. In an October 2026 validation, three agents
were given only a README each and produced nine key frames. Six were near-black with one warm accent
(terracotta, amber, vermilion) and bone-white type; all three directions of one product shared that
pattern, and the user disliked every one of them. Each card said its look "differed from the house
style", because the house style had been described by names (a font, a lime accent), and the agents
avoided the names and kept the pattern.

## 1. Find the colours before choosing any

Work down this list and write where each colour came from (`— from:` on the palette line, §5):

1. **The brand's own values.** Read them; do not eyeball them. Sources: the site's CSS (custom
   properties, the `theme-color` meta, the most frequent hex values in its stylesheet), the logo file,
   the app icon, a brand page. A hex with its source beats any adjective.
2. **The product itself.** Its interface (sample the pixels of real screenshots), its hardware finish,
   the things it makes (a design tool's outputs, a camera's footage). A palette that frames a UI starts
   from that UI's own neutrals, so the interface sits inside the film instead of on top of it.
3. **The world of the idea.** The material the product's name or promise lives in, taken from a real
   reference you can sample: specimen paper and pencil, wet clay, anodised metal, a terminal's phosphor.
   Sample the photograph; do not turn an adjective into a hex.
4. **Invention, last,** and labelled "invented: no brand colours found" on the card.

An open-source project with only a README still has colours to find: its README badges and images, the
outputs it produces, the tools it lives in, the repository's social image. Look before inventing.

## 2. Build a system, not a pick

| Role | Job | Typical share of the frame |
|---|---|---|
| ground | the world the film happens in | most of it |
| surface | panels and cards, one or two steps off the ground | a fifth or so |
| ink, muted ink | type and lines | small |
| accent | one meaning only: the new thing, the action, the result | a few per cent |
| flood (optional) | the accent or a second hue filling the whole screen on a beat | a moment, once or twice |

What separates a designed palette from a generated one:

- **Value first.** The frame reads in greyscale: hierarchy comes from lightness steps, and colour adds
  meaning on top. Desaturate a still and look; if the subject disappears, the palette is doing the
  work that composition should do.
- **Neutrals with a small, deliberate bias.** Most measured films tinted their greys slightly cool
  or warm, rarely more than a whisper (a/b within ±3). An unexamined warm brown-black or cream reads
  as generated. Choose the bias; do not inherit it.
- **Few hue families.** One family plus neutrals, or two families in a chosen relationship
  (complementary for tension, analogous for calm). Three saturated hues of equal weight look cheap.
- **Saturation has one home.** Either a neutral world with one saturated accent, or a saturated field
  behind a neutral subject. Medium saturation everywhere is the mud between the two.
- **Light is part of the colour.** A film's ground is lit: a falloff, a vignette, grain, the glow of a
  screen, all in the same hue. A flat hex fill reads as a slide.
- **Type is neutral.** In 18 of 18 measured films with type, it was neutral white or neutral black,
  often on a neutral black or white field; bone and cream type was not an industry default. Small
  text needs 4.5:1 contrast against its ground; `om swatch` reports it.
- **Content brings its own colour.** Screenshots, footage and outputs already have colour. Keep the
  designed palette quieter than the content it frames.
- **The accent is scarce so that it means something.** If it is on every element, it marks nothing;
  if it floods the screen, that is an event placed on a beat.

## 3. The product's colours first; directions differ in how they use them

A film about a product is in the product's colours: the ones its site, interface, logo and packaging
really use (`om grab` lists them in materials.md, with where each came from). An orange brand stays
orange, a neutral interface with one accent stays that. The three directions differ in language,
structure and material, and in how they use the brand's palette:

- **Product colour.** The interface or finish sets everything (most software, hardware, a strong brand).
- **Neutral world, one signal.** The brand's ground and its one accent, with one meaning.
- **Natural light.** Real footage carries the colour, and the graphics stay neutral.
- **Material.** Paper, metal, clay or glass, photographed or sampled and lit.
- **Colour fields.** Full-screen saturated grounds that switch on the cut. Only when the colours are
  the product's own (its skins, themes, a palette tool) — never invented to add energy; energy comes
  from motion and cutting.

Invent colours only when the product has none of its own to give (a concept, an idea, a brand-new
product without a site), and say so on the card. Then vary the ground's value and hue family across
the directions. `om swatch directions.md` skips its house-look warnings when every palette names a
product source in "— from:", and warns when invented palettes all share one look.

## 4. The house look, as patterns

These combinations make a film interchangeable with what every other agent produces. Avoid them in
invented palettes; when the brand's own values are one of them, use them and say so on the card:

- dark ground, one warm accent (terracotta, amber, vermilion, orange), bone or cream type, often a
  serif display;
- warm off-white or cream ground, a serif or giant grotesk, an orange-red or terracotta accent;
- near-black with an acid lime or green;
- a purple-to-blue gradient; neon on a GitHub-dark ground;
- the same "neutral plus one accent" strategy in every direction.

Changing the hex while keeping the pattern does not count.

## 5. On the direction card

Every direction carries a palette line beside its `look:`:

```
Palette:  ground #EEF0EC 70 · surface #DCE2DA 15 · ink #15201B · accent #2F6BFF 5 · flood #2F6BFF — from: site CSS (--brand), UI screenshot neutrals
```

Roles, hex values, shares of the frame where they matter, and the source after the dash. Run `om
swatch directions.md` and show the PNG beside the key frames. Users choose colour separately from
composition and rhythm ("A's palette with C's composition"), so keep the palette a separate line that
can move between directions.

## 6. What 21 launch films did (measured, 2026-10)

The first 60 s of 21 launch films, frames sampled per shot and clustered in Lab:

- **Colours were found, not invented**, in 19: brand values, the product's finish or interface, the
  light of the footage, generated imagery. Designed-from-nothing palettes: 2.
- **Ground follows what the film carries.** 10 mostly dark, 8 mostly light, 2 mixed; hardware leaned
  dark (6 of 9), software leaned light (5 of 10 light against 3 dark). "Tech needs black" did not hold.
- **The accent was scarce.** In 12 films no frame had more than 5 % of strongly saturated pixels. The
  designed single accents sat on the point being operated: a green dot on the selected file, an
  indigo cursor, an orange outline on the chosen item, each about 1 % of the frame.
- **Floods were rhythm.** Designed full-screen colour appeared in 4 films, all energetic ones
  (three colours rotating behind white cards; five saturated grounds changing on the beat; one hue
  for the whole film).
- **Bursts kept one colour world** as often as not: the change came from the cut, not the colour.
- **The two house patterns** (dark ground with one warm accent and bone type; cream, serif and
  terracotta) appeared in **0 of 21**. Where warmth appeared on dark it came from the product's finish,
  a beam of light or the footage.

## 7. Colour over time

Plan colour per stretch in the rhythm sheet ([rhythm.md](rhythm.md) §7): a ground flip at the stop,
a flood on the drop, colour fields switching through a burst, the brand's ground again at the mark.
A palette that never changes is part of a flat film.

## 8. Check

- Desaturate a key frame: the hierarchy still reads.
- Look at it at phone feed size, on both a light and a dark surround.
- Put it beside the brand's own site or screenshots: does the film look like it belongs to them?
- Judge colour only on frames with final colours and type, never on grey boxes.
