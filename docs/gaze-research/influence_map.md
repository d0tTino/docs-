---
title: "Influence Map"
tags: [gaze, visualization]
project: docs-hub
updated: 2025-08-12
---

--8<-- "_snippets/disclaimer.md"

# Influence Map

Below is a vector diagram mapping key theorists and gaze variants.

![Diagram with a pink Lacan node leading via arrows to a blue Foucault node, an orange Mulvey node, a green hooks node, and a gray algorithmic gaze node, illustrating the flow of theoretical influence](influence-map.svg)

*Figure: Colored nodes trace theoretical traditions—pink for psychoanalysis (Lacan), blue for post-structural power (Foucault), orange for feminist film (Mulvey), green for intersectional feminism (hooks), and gray for the algorithmic gaze. Arrows indicate the flow of influence from earlier to later thinkers.*

The diagram was generated using a short Python script leveraging the `svgwrite` library.

```mermaid
graph LR
    Lacan[Lacan]
    Foucault[Foucault]
    Mulvey[Mulvey]
    hooks[hooks]
    AG[Algorithmic Gaze]

    Lacan --> Foucault --> Mulvey --> hooks --> AG

    style Lacan fill:#f6d,stroke:#000
    style Foucault fill:#9cf,stroke:#000
    style Mulvey fill:#ffd1a9,stroke:#000
    style hooks fill:#cfc,stroke:#000
    style AG fill:#e5e5e5,stroke:#000
```

## Legend

- Pink nodes (e.g., [Lacan](gaze_bibliography.md)) denote psychoanalytic foundations.
- Blue nodes (e.g., [Foucault](gaze_bibliography.md)) mark post-structural power analyses.
- Orange nodes (e.g., [Mulvey](gaze_bibliography.md)) represent feminist film theory.
- Green nodes (e.g., [hooks](gaze_bibliography.md)) highlight intersectional feminism.
- Gray node ([algorithmic gaze](gaze_bibliography.md)) indicates contemporary digital extensions.
- Arrows show the direction of theoretical influence from earlier to later thinkers.
