<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  import DashboardHeader from "$lib/components/Analytics/UI/DashboardHeader.svelte";

  import HealthDonut from "$components/Analytics/Charts/HealthDonut.svelte";
  import BreedDonut from "$components/Analytics/Charts/BreedDonut.svelte";
  import MilkYieldBar from "$components/Analytics/Charts/MilkYieldBar.svelte";
  import WaterIntakeBar from "$components/Analytics/Charts/WaterIntakeBar.svelte";
  import { fetchBreedData } from "$lib/API/AnalyticsAPI/BreedDataAPI.js"; // Add .js potentially 
  import { fetchHealthData } from "$lib/API/AnalyticsAPI/HealthDataAPI.js";
  import { fetchMilkYieldData } from "$lib/API/AnalyticsAPI/MilkYieldDataAPI.js";
  import { fetchWaterData } from "$lib/API/AnalyticsAPI/WaterDataAPI.js";
  import  AuthFetchAPI  from "../../API/AuthenticationAPI/AuthFetchAPI";
  
  import { 
    getHealthChartData,
    getBreedChartData,
    getMilkYieldChartData,
    getWaterIntakeChartData
  } from "$lib/services/analytics";

  let healthData = [];
  let breedData = [];
  let milkData = [];
  let waterData = [];

  onMount(async () => {
    try {
      healthData = await getHealthChartData();
      breedData = await getBreedChartData();
      milkData = await getMilkYieldChartData();
      waterData = await getWaterIntakeChartData();
    } catch (err) {
      console.error("Error loading analytics:", err);
    }
  });

  function navigate(path) {
    goto(path);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    goto("/login");
  }
</script>

<DashboardHeader
  onNavigate={navigate}
  onLogout={logout}
/>

<main class="grid">
  <HealthDonut {healthData} />
  <BreedDonut {breedData} />
  <MilkYieldBar {milkData} />
  <WaterIntakeBar {waterData} />
</main>
