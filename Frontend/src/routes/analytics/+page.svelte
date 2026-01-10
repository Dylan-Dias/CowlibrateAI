<script>
  import { onMount } from "svelte";
  import DashboardHeader from "$lib/components/Analytics/UI/DashboardHeader.svelte";
  import { goto } from '$app/navigation';

  import HealthDonut from "$components/Analytics/Charts/HealthDonut.svelte";
  import BreedDonut from "$components/Analytics/Charts/BreedDonut.svelte";
  import MilkYieldBar from "$components/Analytics/Charts/MilkYieldBar.svelte";
  import WaterIntakeBar from "$components/Analytics/Charts/WaterIntakeBar.svelte";

  let healthData = [];
  let breedData = [];
  let milkData = [];
  let waterData = [];

  onMount(async () => {
    healthData = await fetchHealthData();
    breedData = await fetchBreedData();
    milkData = await fetchMilkYieldData();
    waterData = await fetchWaterData();
  });
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
