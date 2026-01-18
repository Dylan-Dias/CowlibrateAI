<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  // Carbon Layout Components
  import { Grid, Row, Column, Tile } from "carbon-components-svelte";

  import DashboardHeader from "$lib/components/Analytics/UI/DashboardHeader.svelte";
  import HealthMeter from "$components/Analytics/Charts/HealthMeter.svelte";
  import BreedDonut from "$components/Analytics/Charts/BreedDonut.svelte";
  import MilkYieldBar from "$components/Analytics/Charts/MilkYieldBar.svelte";
  import WaterIntakeBar from "$components/Analytics/Charts/WaterIntakeBar.svelte";
  
  // Services
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
      // Parallel fetching is faster
      [healthData, breedData, milkData, waterData] = await Promise.all([
        getHealthChartData(),
        getBreedChartData(),
        getMilkYieldChartData(),
        getWaterIntakeChartData()
      ]);
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

<DashboardHeader onNavigate={navigate} onLogout={logout} />

<div class="dashboard-container">
  <Grid>
    <Row class="chart-row">
      <Column lg={8} md={8} sm={4}>
        <Tile class="chart-tile">
          <HealthMeter {healthData} />
        </Tile>
      </Column>

      <Column lg={8} md={8} sm={4}>
        <Tile class="chart-tile">
          <BreedDonut {breedData} />
        </Tile>
      </Column>
    </Row>

    <Row class="chart-row">
      <Column lg={16} md={8} sm={4}>
        <Tile class="chart-tile">
          <MilkYieldBar {milkData} />
        </Tile>
      </Column>
    </Row>

    <Row class="chart-row">
      <Column lg={16} md={8} sm={4}>
        <Tile class="chart-tile">
          <WaterIntakeBar {waterData} />
        </Tile>
      </Column>
    </Row>
  </Grid>
</div>

<style>
  .dashboard-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background-color: #f4f4f4; /* Light gray background to make Tiles pop */
    min-height: 100vh;
  }

  /* Add spacing between rows */
  :global(.chart-row) {
    margin-bottom: 1.5rem;
  }

  /* Ensure Tiles have a consistent look */
  :global(.chart-tile) {
    height: 100%;
    min-height: 350px; /* Prevents layout shift before chart loads */
    background-color: #ffffff;
  }
</style>