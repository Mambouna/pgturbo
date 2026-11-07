#import "@preview/fletcher:0.5.8": diagram, node, edge

#set page(width: 6cm, height: 1.85cm, fill: none)
#set text(font: "Liberation Sans")
#show raw: set text(weight: "bold")

#align(center + horizon, diagram(
    node((0.75, 0), [Game state]),
    edge("->", bend: 20deg),
    node((1.6, 0.5), [`update()`]),
    edge("->", bend: 20deg),
    node((0.0, 0.5), [`draw()`]),
    edge((0.75, 0), "->", bend: 20deg),
))
