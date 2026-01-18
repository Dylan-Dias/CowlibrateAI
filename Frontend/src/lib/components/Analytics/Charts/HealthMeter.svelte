<script>
  import { MeterChart } from "@carbon/charts-svelte";
  import "@carbon/charts/styles.css";

  export let healthData = []; 
  // Expected input: [{ group: "Healthy", value: 45 }, { group: "Sick", value: 5 }]

  // 1. Calculate the percentage of healthy cows
  $: totalCows = healthData.reduce((acc, item) => acc + item.value, 0);
  $: healthyCount = healthData.find(d => d.group === "Healthy")?.value || 0;
  $: healthPercentage = totalCows > 0 ? Math.round((healthyCount / totalCows) * 100) : 0;

  // 2. Format data for Meter Chart (It expects a single group)
  $: chartData = [
    { group: "Health Score", value: healthPercentage }
  ];

  const options = {
    title: "Herd Health Status",
    height: "150px", // Meters are compact
    meter: {
      peak: 100, // The goal is 100%
      status: {
        // Semantic Colors: Red < 80%, Yellow < 95%, Green > 95%
        ranges: [
          { range: [0, 80], status: "danger" },
          { range: [80, 95], status: "warning" },
          { range: [95, 100], status: "success" }
        ]
      }
    },
    color: {
      scale: {
        "Health Score": "#198038" // Default Green (Carbon Green-60)
      }
    },
    toolbar: { enabled: false } // Hides the menu dots
  };
</script>

<div class="meter-container">
  <MeterChart data={chartData} {options} />
  <p class="summary">
    <strong>{healthyCount}/{totalCows}</strong> cows are healthy
  </p>
</div>

<style>
  .summary {
    text-align: center;
    margin-top: -1rem;
    font-size: 0.875rem;
    color: #525252;
  }
</style>