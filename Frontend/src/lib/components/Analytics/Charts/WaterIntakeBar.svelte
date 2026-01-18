<script>
  import { BarChartSimple } from "@carbon/charts-svelte";
  import "@carbon/charts/styles.css";

  export let waterData = []; 
  // Expected input: [{ group: "Low", value: 5 }, { group: "High", value: 20 }]

  const options = {
    title: "Water Intake Levels",
    height: "300px",
    axes: {
      left: { mapsTo: "value", title: "Count of Cows" },
      bottom: { mapsTo: "group", scaleType: "labels" }
    },
    color: {
      scale: {
        "Low": "#da1e28",    // Danger (Red)
        "Medium": "#f1c21b", // Warning (Yellow)
        "High": "#0f62fe"    // Good (Blue)
      }
    },
    legend: { enabled: false } // The labels "Low/High" explain themselves
  };
</script>

<SimpleBarChart data={waterData} {options} />