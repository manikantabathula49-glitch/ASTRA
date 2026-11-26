# 3d-object — it's a real thing in space

A hero object in 3D — a device, a logo, a numeral, an isometric diorama, a low-poly city — lit,
orbited, assembled, exploded. Includes the Claude Motion city fly-through and the lit studio diorama
with voxel character.

**Says:** *tangible, premium, real, crafted.* Depth gives value.

**Use when:** hardware, physical products, logos and numerals as monuments, spatial data (maps →
cities), premium launches. **Avoid when:** the message lives in UI text (3D makes text hard to read).

## Signature

1. One hero object, soft studio light (key + rim + bounce), contact shadows, real materials.
2. Camera on arcs: slow orbit, dolly in, a reveal from below; parallax with foreground props.
3. Assembly / explode / rotate to reveal facets (a cube whose faces are styles).
4. Matte, paper-model or clay looks avoid uncanny realism and render fast.
5. Flat → 3D transition: a 2D map, logo or chart extrudes into space.
6. Hardware launch arc (CMF Speaker, Oct 2026): material close-ups of one detail → the hero object →
   exploded view of the internals → the lineup floating in colourways → the grid of variants with the
   name → wordmark. Cuts on the beat about every 1.5 s, a loud electronic track, small mono labels
   for the specs (`18-HOUR PLAYBACK`).
7. Engineering ident: monochrome wireframe objects with leader-line callouts that assemble, then
   collapse into the logo's shape (Vercel, Oct 2026). Silent-safe, 12–22 s.

## Camera · rhythm · easing

`power2.inOut` orbits, 2–4 s; quick snaps for beats; depth of field to guide focus.

## Sound

Deep whooshes for camera travel, mechanical clicks for assembly, airy pads.

## Build

Start from `om new <dir> --template object-3d`: a lit studio (`OM3.stage`, `OM3.lights`, `OM3.cyc`), the
product's real screenshot on a device (`OM3.screen`), its icon or logo SVG extruded (`OM3.logo`), panels cut from
the same capture for depth, one camera (`OM.space`) and one clock (`OM3.film`). GLB models with `OM3.gltf`.
Camera moves, the space, materials and the pitfalls: [depth.md](../../depth.md). For an interface rather than an
object, the same camera over CSS 3D layers: `--template ui-space`.

## Breaks when

Default grey lighting; plastic materials; camera spinning with no target; text placed in 3D unreadably.
