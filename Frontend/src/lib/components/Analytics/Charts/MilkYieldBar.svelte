<script>
  import { BarChartSimple } from '@carbon/charts-svelte'

  export let milkData = []; // array of objects { group, key, value }

  const options = {
    title: "Milk Yield",
    height: "300px",
    axes: {
      left: { mapsTo: "value", title: "Liters" },
      bottom: { mapsTo: "key", title: "Cow" }
    },
    bar: { groupSpacing: 0.2 }
  };
</script>

<BarChartSimple data={milkData} {options} />
