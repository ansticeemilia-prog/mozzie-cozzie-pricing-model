# Mozzie Cozzie Pricing Model

Independent project looking at pricing strategy in the UK sustainable/technical outdoor clothing market, using Mozzie Cozzie as the focal brand.

The idea came from wanting to understand how a brand's pricing looks once you account for what it actually costs to make the product, not just the sticker price. Competitors obviously don't publish their real cost structures, so I built a "cost bridge" that works backwards from fabric type, labour cost by manufacturing country, and treatment or construction complexity, to estimate what a garment's implied margin might be.

The data folder has pricing and specs for 7 competitors, all gathered from their own product pages. The scripts folder has the actual model: cost_bridge.py does the cost estimation, pricing_analysis.py runs the full analysis and produces the charts and tables, which land in the outputs folder. research_log.md has notes on where every number came from and where I had to estimate instead.

To run it, cd into scripts and run pricing_analysis.py.

The most interesting result was that once you factor in UK labour costs and the extra construction work behind Mozzie Cozzie's Air-Gap Design (their insect protection comes from a structural gap built into the garment rather than a chemical treatment), the implied margin on the £576 jumpsuit bundle actually comes out ahead of most competitors rather than behind them, which wasn't what I expected going in. I also noticed Páramo, the other sustainability-focused brand in the set, sits at the top of the market on both price and protection rating, which suggests there's room in this segment to charge more without giving anything up on performance.

One thing I had to think through carefully: Mozzie Cozzie sells as a bundle (jumpsuit, hood, mask, bag) while everyone else in the dataset sells single garments, so comparing the bundle price straight to a single shirt isn't really fair. I left it out of the price-vs-protection chart for that reason, but kept it in the margin analysis since that comparison still works fine at the bundle level.

Worth being upfront that the cost inputs (fabric cost per gram, labour cost by country and so on) are my own estimates based on general research, not competitors' actual financials, since nobody publishes that. Where a competitor didn't list something, like a UPF rating or a manufacturing country, I left it blank rather than guess, and just excluded that row from whichever chart specifically needed the missing field. All of that's logged in research_log.md.

Things I'd want to add if I kept going with this: a price elasticity assumption so it models revenue impact and not just margin impact, and a scenario modelling what happens to the sustainability story if manufacturing moved out of the UK.
