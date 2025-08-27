<script>
  import 'carbon-components-svelte/css/g10.css';
  import { Grid, Row, Column, Tile, Button, Header, HeaderNav, HeaderNavItem } from 'carbon-components-svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let ApexCharts;
  let charts = {};

  const chartConfigs = [
    {
      id: "pieChart",
      options: { chart: { type: "pie", height: 300 }, labels: ["Goats", "Cows", "Sheep"], legend: { position: "bottom" }, title: { text: "Breed Distribution", align: "center" } },
      series: [44, 55, 41]
    },
    {
      id: "barChart",
      options: { chart: { type: "bar", height: 300 }, xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] }, title: { text: "Milk Yield (Liters)", align: "center" } },
      series: [{ name: "Milk Yield", data: [30, 40, 35, 50, 49, 60] }]
    },
    {
      id: "lineChart",
      options: { chart: { type: "line", height: 300 }, xaxis: { categories: ["Week 1", "Week 2", "Week 3", "Week 4"] }, stroke: { curve: "smooth" }, title: { text: "Feed Efficiency (%)", align: "center" } },
      series: [{ name: "Efficiency", data: [75, 78, 80, 85] }]
    },
    {
      id: "areaChart",
      options: { chart: { type: "area", height: 300 }, xaxis: { categories: ["Mon", "Tue", "Wed", "Thu", "Fri"] }, title: { text: "Daily Water Intake (Liters)", align: "center" } },
      series: [{ name: "Water", data: [120, 132, 101, 134, 90] }]
    },
    {
      id: "radarChart",
      options: { chart: { type: "radar", height: 300 }, xaxis: { categories: ["Protein", "Fiber", "Fat", "Minerals", "Vitamins"] }, title: { text: "Nutrient Balance", align: "center" } },
      series: [{ name: "Goat Diet", data: [80, 50, 60, 90, 70] }]
    },
    {
      id: "donutChart",
      options: { chart: { type: "donut", height: 300 }, labels: ["Healthy", "Sick", "Observation"], legend: { position: "bottom" }, title: { text: "Health Status Distribution", align: "center" } },
      series: [70, 15, 15]
    }
  ];

  onMount(async () => {
    const module = await import("apexcharts");
    ApexCharts = module.default;

    chartConfigs.forEach(cfg => {
      const chart = new ApexCharts(document.querySelector(`#${cfg.id}`), { ...cfg.options, series: cfg.series });
      chart.render();
      charts[cfg.id] = chart;
    });
  });

  function navigateTo(path) {
    goto(path);
  }

  async function generateReport() {
    const { jsPDF } = await import("jspdf");
    const html2canvas = (await import("html2canvas")).default;

    const pdf = new jsPDF("p", "pt", "a4");
    const dashboardEl = document.querySelector("#dashboard");

    const canvas = await html2canvas(dashboardEl, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");

    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("Goat-Analytics-Report.pdf");
  }
</script>

<!-- NAV BAR -->
<Header company="CowlibrateAI Dashboard" class="nav-bar">
  <HeaderNav>
    <HeaderNavItem on:click={() => navigateTo('/dashboard/goat')}>Goat Input</HeaderNavItem>
    <HeaderNavItem on:click={generateReport}>Generate Report</HeaderNavItem>
          <HeaderNavItem on:click={logout}>Logout</HeaderNavItem>


  </HeaderNav>
</Header>

<!-- DASHBOARD -->
<main id="dashboard">
  <Grid>
    <Row>
      {#each chartConfigs as cfg}
        <Column sm="4" md="4" lg="4">
          <Tile>
            <h2>{cfg.options.title?.text || "Chart"}</h2>
            <div id={cfg.id} class="chart-container"></div>
          </Tile>
        </Column>
      {/each}
    </Row>
  </Grid>
</main>

<style>


  :global(.bx--header__name) {
    color: white !important;
    font-weight: 700;
  }

  :global(.bx--header__nav-item) {
    color: white !important;
  }

  :global(.bx--header__nav-item:hover) {
    color: #4fc3f7 !important;
  }

  :global(.bx--tile) {
    padding: 1rem 1.5rem;
    background: #f4f4f4;
  }

  h2 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: #222;
    font-weight: 600;
    text-align: center;
  }

  .chart-container {
    width: 100%;
    height: 300px;
    min-height: 300px;
    border-radius: 8px;
    background-color: white;
    box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.05);
  }
</style>
