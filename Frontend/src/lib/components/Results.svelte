<script>
  import 'carbon-components-svelte/css/g10.css';
  import {
    DataTable,
    TableContainer,
    Table,
    TableHead,
    TableRow,
    TableHeader,
    TableBody,
    TableCell
  } from 'carbon-components-svelte';
  import { goto } from '$app/navigation';

  export let selectedCows = [];

  // Define table headers to match the cow data keys
  const headers = [
    { header: 'ID', key: 'id' },
    { header: 'Breed', key: 'breed' },
    { header: 'Milk Yield', key: 'milk_yield' },
    { header: 'Health', key: 'health' },
    { header: 'Lactation Stage', key: 'lactation_stage' },
    { header: 'Age', key: 'age' }
  ];
</script>

<main>
  <h1>Optimization Results</h1>
  {#if selectedCows.length === 0}
    <p>No optimized cows selected yet.</p>
  {:else}
    <TableContainer title="Selected Cows for Milk Optimization">
      <DataTable rows={selectedCows} headers={headers} let:rows let:headers>
        <Table>
          <TableHead>
            <TableRow>
              {#each headers as header}
                <TableHeader>{header.header}</TableHeader>
              {/each}
            </TableRow>
          </TableHead>
          <TableBody>
            {#each rows as row}
              <TableRow>
                {#each headers as header}
                  <TableCell>{row[header.key]}</TableCell>
                {/each}
              </TableRow>
            {/each}
          </TableBody>
        </Table>
      </DataTable>
    </TableContainer>
  {/if}
</main>

<style>
  main {
    max-width: 900px;
    margin: 2rem auto;
    padding: 1rem;
  }
  h1 {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  p {
    text-align: center;
    font-style: italic;
    color: #666;
  }
</style>
