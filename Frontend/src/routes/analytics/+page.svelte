<script>
  import { onMount } from "svelte";
  import DashboardHeader from "$lib/components/Analytics/UI/DashboardHeader.svelte";
  import { goto } from '$app/navigation';

  import HealthDonut from "$components/Analytics/Charts/HealthDonut.svelte";
  import BreedDonut from "$components/Analytics/Charts/BreedDonut.svelte";
  import MilkYieldBar from "$components/Analytics/Charts/MilkYieldBar.svelte";
  import WaterIntakeBar from "$components/Analytics/Charts/WaterIntakeBar.svelte";


  import { getBreedChartData } from "$lib/services/analytics";
  import { getHealthChartData } from "$lib/services/analytics";
  import { getMilkYieldChartData } from "$lib/services/analytics";
  import { getWaterIntakeChartData} from "$lib/services/analytics";

  let healthData = [];
  let breedData = [];
  let milkData = [];
  let waterData = [];

  onMount(async () => {
  try {
    breedData = await getBreedChartData();
  } catch (err) {
    console.error(err);
  }
});

  onMount(async () => {
  try {
    breedData = await getHealthChartData();
  } catch (err) {
    console.error(err);
  }
});

  onMount(async () => {
  try {
    breedData = await getMilkYieldChartData();
  } catch (err) {
    console.error(err);
  }
});

  onMount(async () => {
  try {
    breedData = await getWaterIntakeChartData();
  } catch (err) {
    console.error(err);
  }
});



  onMount(async () => {
    try {
    healthData = await fetchHealthData();
    breedData = await fetchBreedData();
    milkData = await fetchMilkYieldData();
    waterData = await fetchWaterData();
    } catch (err) {
      console.error('Error loading analytics:', err);
  }
  });



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



<main class="grid">
  <HealthDonut {healthData} />
  <BreedDonut {breedData} />
  <MilkYieldBar {milkData} />
  <WaterIntakeBar {waterData} />
</main>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }
</style>
