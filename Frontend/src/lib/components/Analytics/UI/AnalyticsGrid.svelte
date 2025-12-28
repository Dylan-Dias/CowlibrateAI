<script>
  import { Grid, Row, Column } from 'carbon-components-svelte';
  import ChartTile from './ChartTile.svelte';
  export let charts = [];
</script>

<Grid>
  {#each [0,1] as rowIndex}
    <Row>
      {#each charts.slice(rowIndex*3, rowIndex*3+3) as cfg}
        <Column sm="4" md="4" lg="4">
          <ChartTile title={cfg.title} chartId={cfg.id} />
        </Column>
      {/each}
    </Row>
  {/each}
</Grid>

<style>
  :global(.bx--grid) {
    margin-top: 2rem;
  }

  :global(.bx--row) {
    margin-bottom: 2rem;
  }
</style>

