<script>
  export let title = "";
  export let chartId = "";
  
</script>

<div class="chart-tile">
  <h2>{title}</h2>
  <div id={chartId} class="chart-container"></div>
</div>

<style>


  h2 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: #222;
    font-weight: 600;
    text-align: center;
  }

  .chart-container {
    width: 100%;
    height: 300px;
    min-height: 300px;
    border-radius: 8px;
    background-color: white;
    box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.05);
  }
</style>
