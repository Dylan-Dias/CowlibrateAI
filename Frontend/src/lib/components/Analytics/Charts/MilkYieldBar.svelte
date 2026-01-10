<script>
  import { BarChart } from "@carbon/charts-svelte";

  export let milkData = [];

  const options = {
    title: "Milk Yield Distribution",
    axes: {
      left: { mapsTo: "value", title: "Liters" },
      bottom: { mapsTo: "key", scaleType: "labels", title: "Cow" }
    },
    height: "300px"
  };
</script>

<BarChart data={milkData} {options} />
