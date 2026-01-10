<script>
  import { DonutChart } from "@carbon/charts-svelte";

  export let breedData = [];

  const options = {
    title: "Breed Distribution",
    resizable: true,
    height: "300px"
  };
</script>

<DonutChart data={breedData} {options} />
