
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Star Schema Teaching Bundle";

const FONT = "Calibri";
const TITLE_SIZE = 38;
const H2_SIZE = 24;
const BODY_SIZE = 16;

function addTitle(slide, title, subtitle) {
  slide.addText(title, { x: 0.6, y: 0.5, w: 12.1, h: 0.8, fontFace: FONT, fontSize: TITLE_SIZE, bold: true });
  if (subtitle) {
    slide.addText(subtitle, { x: 0.6, y: 1.35, w: 12.1, h: 0.6, fontFace: FONT, fontSize: 18, color: "444444" });
  }
}

function addBullets(slide, heading, bullets, yStart=1.0) {
  slide.addText(heading, { x: 0.8, y: yStart, w: 12.0, h: 0.5, fontFace: FONT, fontSize: H2_SIZE, bold: true });
  slide.addText(bullets.join("\n"), {
    x: 1.1, y: yStart + 0.7, w: 11.6, h: 5.1,
    fontFace: FONT, fontSize: BODY_SIZE,
    bullet: { indent: BODY_SIZE * 1.2 },
    paraSpaceAfter: 8
  });
}

function addCode(slide, heading, code, y=0.9) {
  slide.addText(heading, { x: 0.8, y: y, w: 12.0, h: 0.5, fontFace: FONT, fontSize: H2_SIZE, bold: true });
  slide.addShape(pptx.ShapeType.rect, { x: 0.8, y: y+0.7, w: 12.0, h: 5.7, fill: { color: "F5F7FA" }, line: { color: "D0D7DE" } });
  slide.addText(code, {
    x: 1.0, y: y+0.9, w: 11.6, h: 5.3,
    fontFace: "Consolas", fontSize: 12, color: "111111"
  });
}

function addStarDiagram(slide) {
  slide.addText("Star Schema: Visual Overview", { x: 0.8, y: 0.6, w: 12.0, h: 0.5, fontFace: FONT, fontSize: H2_SIZE, bold: true });
  slide.addShape(pptx.ShapeType.roundRect, { x: 5.3, y: 2.4, w: 3.0, h: 1.0, fill: { color: "1F77B4" }, line: { color: "1F77B4" } });
  slide.addText("FACT_SALES\n(measures)", { x: 5.3, y: 2.45, w: 3.0, h: 1.0, fontFace: FONT, fontSize: 16, color: "FFFFFF", align: "center", valign: "mid", bold: true });

  const dims = [
    { title: "DIM_DATE", x: 5.3, y: 1.2 },
    { title: "DIM_CUSTOMER", x: 1.4, y: 2.4 },
    { title: "DIM_PRODUCT", x: 9.2, y: 2.4 },
    { title: "DIM_STORE", x: 5.3, y: 3.8 }
  ];

  dims.forEach(d => {
    slide.addShape(pptx.ShapeType.roundRect, { x: d.x, y: d.y, w: 3.0, h: 0.8, fill: { color: "2CA02C" }, line: { color: "2CA02C" } });
    slide.addText(d.title, { x: d.x, y: d.y+0.1, w: 3.0, h: 0.6, fontFace: FONT, fontSize: 16, color: "FFFFFF", align: "center", valign: "mid", bold: true });
  });

  slide.addShape(pptx.ShapeType.line, { x: 6.8, y: 2.4, w: 0, h: -0.4, line: { color: "666666", width: 2 } });
  slide.addShape(pptx.ShapeType.line, { x: 5.3, y: 2.9, w: -0.9, h: 0, line: { color: "666666", width: 2 } });
  slide.addShape(pptx.ShapeType.line, { x: 8.3, y: 2.9, w: 0.9, h: 0, line: { color: "666666", width: 2 } });
  slide.addShape(pptx.ShapeType.line, { x: 6.8, y: 3.4, w: 0, h: 0.4, line: { color: "666666", width: 2 } });

  slide.addText("Fact keys → dimensions\nDimensions provide filter/group-by context", {
    x: 0.9, y: 5.7, w: 12.0, h: 0.8, fontFace: FONT, fontSize: 14, color: "444444"
  });
}

// Slide 1
{
  const s = pptx.addSlide();
  addTitle(s, "Star Schema: From OLTP to Analytics", "Design • ETL • SCD Type 2 • OLAP");
  s.addText("Teaching deck + lab-ready bundle", { x: 0.6, y: 2.1, w: 12.1, h: 0.5, fontFace: FONT, fontSize: 18, color: "333333" });
}

// Slide 2
{
  const s = pptx.addSlide();
  addBullets(s, "Agenda", [
    "Dimensional modeling overview",
    "Fact vs dimension (+ grain)",
    "Star schema structure & benefits",
    "OLTP → DW mapping & ETL",
    "SCD Type 2",
    "Star vs Snowflake",
    "OLAP query patterns",
    "Lab flow"
  ]);
}

// Slide 3
{
  const s = pptx.addSlide();
  addBullets(s, "OLTP vs OLAP", [
    "OLTP: normalized, many small writes, low-latency transactions",
    "OLAP: scans + joins + aggregations across large history",
    "Star schema reduces join complexity and speeds BI queries"
  ]);
}

// Slide 4
{
  const s = pptx.addSlide();
  addBullets(s, "Fact vs Dimension", [
    "Fact: measurable events (sales, shipments, clicks)",
    "Dimensions: descriptive context (who/what/when/where)",
    "Fact tables are large; dimensions are small-ish and descriptive"
  ]);
}

// Slide 5
{
  const s = pptx.addSlide();
  addBullets(s, "Grain (Define it first)", [
    "Grain = what a single fact row represents",
    "Example grain: one row per order_item",
    "Grain determines valid measures and joins",
    "Changing grain later usually requires re-ETL"
  ]);
}

// Slide 6
{
  const s = pptx.addSlide();
  addStarDiagram(s);
}

// Slide 7
{
  const s = pptx.addSlide();
  addBullets(s, "Example Source Tables (OLTP)", [
    "customers(customer_id, first_name, last_name, email, country)",
    "products(product_id, product_name, category, brand, price)",
    "stores(store_id, store_name, region)",
    "orders(order_id, customer_id, store_id, order_date)",
    "order_items(order_item_id, order_id, product_id, quantity, unit_price)"
  ]);
}

// Slide 8
{
  const s = pptx.addSlide();
  addBullets(s, "Mapping to the Star", [
    "dim_date: calendar fields used for time slicing",
    "dim_product: category, brand, product_name",
    "dim_store: region, store_name",
    "dim_customer: SCD2 (tracks country changes, etc.)",
    "fact_sales: measures at order-item grain"
  ]);
}

// Slide 9
{
  const s = pptx.addSlide();
  addBullets(s, "ETL Order (Recommended)", [
    "1) dim_date (generate calendar)",
    "2) Type 1 dims (product, store)",
    "3) Type 2 dims (customer history)",
    "4) fact table (lookup surrogate keys)",
    "5) Validate: counts + FK coverage"
  ]);
}

// Slide 10
{
  const s = pptx.addSlide();
  addBullets(s, "Surrogate Keys", [
    "Warehouse-generated keys (customer_key, product_key, ...)",
    "Enable history (SCD2) while keeping stable joins",
    "Avoid natural key changes breaking historical reporting"
  ]);
}

// Slide 11
{
  const s = pptx.addSlide();
  addBullets(s, "SCD Type 2 (Concept)", [
    "Track attribute history (e.g., customer country changes)",
    "Expire current row + insert new version",
    "Columns: effective_date, expiry_date, is_current",
    "Facts can join to correct version by date range"
  ]);
}

// Slide 12
{
  const s = pptx.addSlide();
  addCode(s, "SCD2 Update + Insert Pattern", 
`-- expire current
UPDATE dim_customer
SET expiry_date = CURDATE() - INTERVAL 1 DAY,
    is_current  = FALSE
WHERE customer_id = 101 AND is_current = TRUE;

-- insert new version
INSERT INTO dim_customer(customer_id, first_name, last_name, email, country, effective_date, expiry_date, is_current)
VALUES (101, 'John', 'Smith', 'john@example.com', 'Canada', CURDATE(), '9999-12-31', TRUE);`);
}

// Slide 13
{
  const s = pptx.addSlide();
  addBullets(s, "Star vs Snowflake", [
    "Star: denormalized dimensions → fewer joins → simpler and often faster",
    "Snowflake: normalized dimensions → more joins → less redundancy",
    "Use Star for BI dashboards and self-serve analytics",
    "Use Snowflake when dimensions are huge or heavily shared"
  ]);
}

// Slide 14
{
  const s = pptx.addSlide();
  addBullets(s, "OLAP Query Patterns", [
    "Roll-up / drill-down (day → month → year)",
    "Slice/dice (filter by region/category and regroup)",
    "Top-N (products, customers)",
    "Growth trends (MoM/YoY) using window functions"
  ]);
}

// Slide 15
{
  const s = pptx.addSlide();
  addBullets(s, "Performance Tips", [
    "Index fact foreign keys",
    "Consider partitioning by date at scale",
    "Pre-aggregate frequent dashboard queries",
    "Validate ETL with counts + null key checks"
  ]);
}

// Slide 16
{
  const s = pptx.addSlide();
  addBullets(s, "Lab Flow", [
    "Lab 1: Generate OLTP dataset",
    "Lab 2: Define grain + map facts/dims",
    "Lab 3: Create DW schema",
    "Lab 4: Load with ETL",
    "Lab 5: Run OLAP queries",
    "Lab 6: Simulate SCD2 change"
  ]);
}

// Slide 17
{
  const s = pptx.addSlide();
  addBullets(s, "Wrap-Up", [
    "Star schema = analytics-friendly structure",
    "Grain drives correctness",
    "ETL turns model into reality",
    "SCD2 enables trustworthy historical reporting"
  ]);
}

pptx.writeFile({ fileName: process.argv[2] || "06_star_schema_teaching_slides.pptx" });
