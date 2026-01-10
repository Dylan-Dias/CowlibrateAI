<script>
  import { BarChart } from "@carbon/charts-svelte";

  export let waterData = [];

  const options = {
    title: "Water Intake Levels",
    axes: {
      left: { mapsTo: "value", title: "Count" },
      bottom: { mapsTo: "key", scaleType: "labels" }
    },
    height: "300px"
  };
</script>

<BarChart data={waterData} {options} />
