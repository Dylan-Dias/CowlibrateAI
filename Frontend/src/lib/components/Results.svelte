<h2>Optimization Results</h2>

{#if results.length > 0}
  <table>
    <thead>
      <tr>
        <th>Cow ID</th>
        <th>Breed</th>
        <th>Milk Yield</th>
        <th>Health</th>
        <th>Lactation Stage</th>
        <th>Age</th>
        <th>Score</th>
      </tr>
    </thead>
    <tbody>
      {#each results as r}
        <tr>
          <td>{r.cow_id}</td>
          <td>{r.breed}</td>
          <td>{r.milk_yield}</td>
          <td>{r.health}</td>
          <td>{r.lactation_stage}</td>
          <td>{r.age}</td>
          <td>{r.score}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>No results yet.</p>
{/if}
