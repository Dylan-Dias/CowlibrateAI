<script>
  import { DonutChart } from "@carbon/charts-svelte";
  import "@carbon/charts/styles.css";

  export let breedData = [];
  // Expected input: [{ group: "Angus", value: 20 }, { group: "Holstein", value: 50 }]

  const options = {
    title: "Breed Distribution",
    resizable: true,
    height: "300px",
    donut: {
      center: {
        label: "Heads" // Text inside the hole
      }
    },
    legend: {
      position: "right" // 'right' or 'bottom' is cleaner than 'left'
    }
  };
</script>

<DonutChart data={breedData} {options} />