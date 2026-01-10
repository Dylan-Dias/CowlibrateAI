<script>
  import { BarChartSimple } from "@carbon/charts-svelte";

  export let waterData = []; // array of objects { group, key, value }

  const options = {
    title: "Water Intake Levels",
    height: "300px",
    axes: {
      left: { mapsTo: "value", title: "Count" },
      bottom: { mapsTo: "key", title: "Level" }
    },
    bar: { groupSpacing: 0.2 }
  };
</script>

<BarChartSimple data={waterData} {options} />
