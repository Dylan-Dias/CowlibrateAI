<script>
  import { BarChartSimple } from "@carbon/charts-svelte";
  import "@carbon/charts/styles.css";

  export let milkData = []; 
  // Expected input: [{ key: "Cow 101", value: 24 }, { key: "Cow 102", value: 12 }...]

  // 1. Sort data by Yield (High to Low)
  $: sortedData = [...milkData].sort((a, b) => b.value - a.value);
  
  // 2. Slice the Top 5 and Bottom 5
  $: topAndBottomData = (() => {
    if (sortedData.length <= 10) return sortedData; // If few cows, show all
    
    // Add a 'group' property so we can color them differently
    const top5 = sortedData.slice(0, 5).map(d => ({ ...d, group: "Top Performers" }));
    const bottom5 = sortedData.slice(-5).map(d => ({ ...d, group: "Needs Attention" }));
    
    return [...top5, ...bottom5];
  })();

  const options = {
    title: "Production Leaders vs. Laggards",
    height: "400px",
    axes: {
      left: { mapsTo: "key", scaleType: "labels", title: "Cow ID" }, 
      bottom: { mapsTo: "value", title: "Liters per Day" }
    },
    color: {
      scale: {
        "Top Performers": "#198038",   // Green
        "Needs Attention": "#da1e28"   // Red
      }
    },
    legend: { position: "top" }
  };
</script>

<BarChartSimple data={topAndBottomData} {options} />