# Depth — the interface in space, real objects in a real space

A product film that only slides flat panels around reads as slides, however well it is cut. Depth is what makes
a shot feel built: the camera swings round the interface, layers of it separate and pass each other, the
product's logo stands as an object with light on its edges, the frame has a foreground, a subject and a
background moving at different speeds. It is one of the three directions the user is offered — always one of
them, never all three, and recommended only when the product and the brief suit it (a premium launch, an
object, an interface with layers worth separating). When it is chosen, it carries the whole film (below).

## Two routes, one camera

| | **Interface in space** (CSS 3D) | **Objects in a studio** (Three.js) |
|---|---|---|
| What | The real interface as layers in depth: screenshots, crops of them, pieces rebuilt in code | The product's things as objects: its logo SVG extruded, its screenshots on a device or cards, its GLB |
| Start | `om new <dir> --template ui-space` | `om new <dir> --template object-3d` |
| Good at | UI films: sharp text at any distance, every piece pickable and editable, real layouts | Hero shots, logos, hardware, a premium launch, light and material, a space you travel through |
| Weak at | Light, shadow, materials (it is paper in space) | Reading UI text up close (use a DOM layer on top, or a canvas texture for a short label) |

Both are driven by **`OM.space`** ([contract](contract.md)): a pose is a target, a distance, yaw, pitch, roll and a
field of view; moves interpolate the angles and the distance, so the camera travels on arcs. The same moves
read the same in either route, and `cam.attach(threeCamera)` puts a WebGL layer behind a page world in sync.
A film can use both: a 3D opening on the logo, then the interface in space.

## The camera — strong moves that still read

Every move has a subject and ends on something. Starting points, not rules:

- **Swing reveal (an opening).** Frame 1 close and oblique on the real thing (distance a third of the final,
  yaw 40–55°, a few degrees of roll), then `expo.out` over 1.5–1.8 s to the establishing angle. The first
  second carries most of the film's motion; the frame is already full of the product.
- **Orbit drift.** During a hold, yaw 10–25° with `sine.inOut`: layers slide past each other (parallax) and the
  object turns its light. A hold without it is dead time.
- **Push to a detail.** `fit` the element (or target it with a smaller distance) in 0.9–1.3 s `expo.inOut`; in a
  studio the focus follows the target (OM3.film focuses at the camera's distance), so the push is also a rack focus.
- **Crane / pull-back.** Distance ×1.5–2, pitch up 15–25°, yaw across 30–50° in about 2 s: shows the space and
  the whole object after a close section.
- **Land.** The last move settles on the hero frame: the object to one side, the type on the other. On a page,
  `flat: true` lands exactly on the layout — layers collapsing into the flat interface is a strong ending.
- **Snap (on a beat).** 0.3–0.5 s `expo.inOut` to a new angle on a hit; once or twice a film.
- Never spin without a target, never cut straight through an object, never end a move on empty space.
  Frames where a dark side or the back of a slab fills the screen read as a black flash: check the first frame
  and the middle of every swing with `om still`.

## When depth is chosen, the whole film is in space

The test films that took the depth direction opened in 3D, then went back to flat cuts for the middle and
the end: depth as a trick for the first two seconds. A depth film is one space the camera travels through:

- **Every stretch has a camera move in space.** Lists, proofs and features are stations in the same world
  (cards standing in depth, panels lifted off the interface, objects on the studio floor), and the camera
  travels from one to the next — an orbit through a row, a push past a near layer into the next, a crane
  over all of them. A cut is fine (on the beat), but the shot after it is also in space.
- **Transitions go through space**: fly through a layer into what is behind it, pull back until the last
  scene is one card among many, rack focus from near to far, whip-pan along the row. Prefer these to 2D
  wipes and swaps.
- **Flat is the exception, used as contrast**: one deliberate flat beat (a slammed word, the pause before
  the drop) at most, then back into space. The end can land flat (`flat: true`) — a landing, not an escape.
- **Plan it in the treatment**: the rhythm sheet names the camera move of every stretch and where each
  station sits in the world (x, y, z), so the film is one route, not a deck with a 3D cover.
- **Check it**: `om still` a frame from every stretch; if a stretch's frame could be a flat slide, give it
  its move.

## A fine space

What separates "a model in a void" from a place:

- **A floor and a wall that don't end.** `OM3.cyc` (a photo-studio sweep) in the product's ground colour; the
  object's soft shadow on it (`OM3.lights`). A hard horizon or a black void reads as unfinished.
- **Light with dark parts.** The default `studio` environment has two soft boxes and a dark floor: metals read as
  metal. All-bright makes them white and weightless; none at all turns them black (on white backgrounds too).
  A real HDR environment (Poly Haven, CC0) goes in with `env: 'assets/x.hdr'`.
- **Layers in depth.** Things at three distances: something close (it passes the lens during moves), the
  subject, something behind. Crops of the same screenshot (`OM3.screen(img, { crop })`, or `background-position`
  on a page) are real material that costs nothing. On a page, lift the panels of the interface apart in z
  (60–400 px) and let them settle.
- **Depth of field** follows the camera's target. Keep `aperture` small (0.002–0.003): blur that hides the
  product is worse than none.
- **Small life.** Objects float a few hundredths of a unit, a panel turns a degree: a still object in a moving
  camera is fine, a still frame is not.
- **Materials:** a device body clearcoated and slightly metallic, screens unlit (`toneMapped: false` — the
  interface keeps its real colours), a faint glass over a screen to catch the studio, logos in their own colours.

## Real material in 3D

- The logo: the real SVG, extruded (`OM3.logo(svg, { size, depth, bevel })`), every filled path in its own colour.
  Never retype or redraw a logo as 3D text.
- The interface: real captures on a device or as floating cards (`OM3.screen`); in a page world, the capture
  cut into layers; pieces that must change (typing, a reply arriving, a number counting) rebuilt in code, traced
  from the capture at the same size.
- Product objects: the product's own GLB if it has one (`OM3.gltf('assets/x.glb')`, one file with its textures).
  Otherwise build from the product's real shapes (its icon paths, its screens), not a stock model.
- Text in WebGL: short labels on a canvas texture after `document.fonts.load` (through `OM3.ready`); anything
  longer stays in the DOM over the canvas.

## How it stays right

- Films render from `file://`: `fetch()` cannot read local files there. `OM3.read`/`OM3.gltf`/HDR use XHR and
  blob URLs; images load through `<img>`. A `.gltf` with separate files will not load: export a `.glb`.
- Every load goes through `OM3.ready` (the helpers do it): the render waits for it, and the films redraw when it
  lands, so no frame is captured before a texture arrives.
- The WebGL frame is drawn after the seek has set every tween (`OM3.film`); move objects from tweened values in
  its `update(t)`, not in your own clock.
- Crop coordinates come from measuring the capture's pixels (where a panel's border or background starts), never
  from eyeballing a scaled preview.
- A page world flattens when an element between the world and a layer has `overflow` other than visible,
  `filter`, `opacity < 1` or a blend mode; put those on the layer itself. Layers must stay in front of the camera.
  Put transforms on positioned elements (`OM.space` measures through them).
- Rendering is software WebGL in a headless browser and is fast enough (a 1080p studio with shadows and depth of
  field renders 11 s in under 10 s on a laptop); `om render --blur` adds motion blur to fast swings.
