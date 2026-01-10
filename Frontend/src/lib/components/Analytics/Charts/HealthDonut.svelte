<script>
  import { DonutChart } from "@carbon/charts-svelte";

  export let healthData = [];

  const options = {
    title: "Health Distribution",
    resizable: true,
    donut: {
      center: {
        label: "Cows"
      }
    },
    height: "300px"
  };
</script>

<DonutChart {options} data={healthData} />
