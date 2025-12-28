<script>
  import 'apexcharts/dist/apexcharts.css';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  import DashboardHeader from '$lib/components/Analytics/UI/DashboardHeader.svelte';
  import AnalyticsGrid from '$lib/components/Analytics/UI/AnalyticsGrid.svelte';
  import ChartTile from '$components/Analytics/UI/ChartTile.svelte';

  let ApexCharts;
  let chartsInstances = {};

  const chartConfigs = [
    { id: "pieChart",  options: { chart: { type: "pie", height: 300 }, legend: { position: "bottom" } }, series: [] },
    { id: "barChart",  options: { chart: { type: "bar", height: 300 }, xaxis: { categories: [] } }, series: [{ name: "Milk Yield", data: [] }] },
    { id: "lineChart",  options: { chart: { type: "line", height: 300 }, xaxis: { categories: ["Week 1", "Week 2", "Week 3", "Week 4"] }, stroke: { curve: "smooth" } }, series: [{ name: "Efficiency", data: [75, 78, 80, 85] }] },
    { id: "areaChart",  options: { chart: { type: "area", height: 300 }, legend: { position: "bottom" } }, series: [] },
    { id: "radarChart",  options: { chart: { type: "radar", height: 300 }, xaxis: { categories: ["Protein", "Fiber", "Fat", "Minerals", "Vitamins"] } }, series: [{ name: "Bovine Diet", data: [80, 50, 60, 90, 70] }] },
    { id: "donutChart",  options: { chart: { type: "donut", height: 300 }, legend: { position: "bottom" } }, series: [] }
  ];

  onMount(async () => {
    try {
      const module = await import("apexcharts");
      ApexCharts = module.default || module;

      chartConfigs.forEach(cfg => {
        const el = document.querySelector(`#${cfg.id}`);
        if (!el) return console.error(`Chart container not found: ${cfg.id}`);
        const chart = new ApexCharts(el, { ...cfg.options, series: cfg.series, title: { text: cfg.title, align: "center" } });
        chart.render();
        chartsInstances[cfg.id] = chart;
      });

      await fetchDonutData();
      await fetchPieData();
      await fetchAreaData();
      await fetchMilkYieldData();

    } catch (err) {
      console.error("Error initializing charts:", err);
    }
  });

async function fetchMilkYieldData() {
  try {
    const token = localStorage.getItem("token"); 
    if (!token) throw new Error("User not authenticated");

    const res = await fetch("http://127.0.0.1:8080/MilkYield-distribution", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Failed to fetch milk yield distribution");

    const data = await res.json();

    chartsInstances["barChart"]?.updateOptions({
    xaxis: { categories: data.labels || [] }
  });


   chartsInstances["barChart"]?.updateSeries([
  { name: "Milk Yield", data: Array.isArray(data.series) ? data.series : [] }
]);


  } catch (err) {
    console.error("Error fetching milk yield data:", err.message);
  }
}

async function fetchDonutData() {
  try {
    const token = localStorage.getItem("token"); // get JWT token
    if (!token) throw new Error("User not authenticated");

    const res = await fetch("http://127.0.0.1:8080/health-distribution", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Failed to fetch health distribution");

    const data = await res.json();
    chartsInstances["donutChart"]?.updateOptions({ labels: data.labels || [] });
    chartsInstances["donutChart"]?.updateSeries(data.series || []);
  } catch (err) {
    console.error("Error fetching donut data:", err.message);
  }
}

async function fetchPieData() {
  try {
    const token = localStorage.getItem("token");
    if (!token) throw new Error("User not authenticated");

    const res = await fetch("http://127.0.0.1:8080/breed-distribution", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Failed to fetch breed distribution");

    const data = await res.json();
    chartsInstances["pieChart"]?.updateOptions({ labels: Array.isArray(data.labels) ? data.labels : [] });
    chartsInstances["pieChart"]?.updateSeries(Array.isArray(data.series) ? data.series : []);
  } catch (err) {
    console.error("Error fetching pie data:", err.message);
    // fallback empty chart so ApexCharts doesn't crash
    chartsInstances["pieChart"]?.updateOptions({ labels: [] });
    chartsInstances["pieChart"]?.updateSeries([]);
  }
}

async function fetchAreaData() {
  try {
    const token = localStorage.getItem("token");
    if (!token) throw new Error("User not authenticated");

    const res = await fetch("http://127.0.0.1:8080/water-intake", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!res.ok) throw new Error("Failed to fetch water intake");

    const data = await res.json();
    chartsInstances["areaChart"]?.updateOptions({ labels: Array.isArray(data.labels) ? data.labels : [] });
    chartsInstances["areaChart"]?.updateSeries(Array.isArray(data.series) ? data.series : []);
  } catch (err) {
    console.error("Error fetching area chart data:", err.message);
    chartsInstances["areaChart"]?.updateOptions({ labels: [] });
    chartsInstances["areaChart"]?.updateSeries([]);
  }
}

  

  function navigate(path) { goto(path); }

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

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    goto("/login");
  }
</script>

<DashboardHeader 
  onNavigate={navigate} 
  onGenerateReport={generateReport} 
  onLogout={logout} 
/>
<style>
  main#dashboard {
    max-width: 1200px;
    width: 90%;
    margin: 5rem auto 3rem;
    padding: 1rem;
  }
</style>


<main id="dashboard">
  <AnalyticsGrid charts={chartConfigs} />
</main>
