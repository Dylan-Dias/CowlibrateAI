<script>
  import {
    Tile, Grid, Row, Column,
    DataTable,
    Button, TextInput,
    Pagination,
    DatePicker, DatePickerInput,
    Tag
  } from "carbon-components-svelte";
  
  // Icons for cleaner UI
  import { Edit, Save, Close, Checkmark } from "carbon-icons-svelte";

  export let entries = [];

  /* --- State & Logic (Kept exactly as you had it) --- */
  let editing = null;
  let editedRow = {};
  let pageSize = 5;
  let page = 1;
  let startDate = null;
  let endDate = null;

  function startEdit(submissionId, type, index) {
    editing = { submissionId, type, index };
    const submission = entries.find(s => s.id === submissionId);
    if (type === "bovine") editedRow = { ...submission.bovines[index] };
    if (type === "feed") editedRow = { ...submission.feeds[index] };
  }

  function saveEdit(submissionId, type, index) {
    const submission = entries.find(s => s.id === submissionId);
    if (type === "bovine") submission.bovines[index] = editedRow;
    if (type === "feed") submission.feeds[index] = editedRow;
    editing = null;
    // TODO: PUT request
  }

  /* Filters */
  $: filteredEntries = entries.filter(e => {
    if (!startDate && !endDate) return true;
    const created = new Date(e.created_at);
    if (startDate && created < startDate) return false;
    if (endDate && created > endDate) return false;
    return true;
  });

  /* Pagination */
  $: pagedEntries = filteredEntries.slice(
    (page - 1) * pageSize,
    page * pageSize
  );

  // Headers for Carbon DataTable
  const bovineHeaders = [
    { key: "id", value: "ID" },
    { key: "milk_yield", value: "Yield" },
    { key: "health", value: "Health" },
    { key: "breed", value: "Breed" },
    { key: "lactation_stage", value: "Lactation" },
    { key: "age", value: "Age" },
    { key: "actions", value: "" },
  ];

  const feedHeaders = [
    { key: "feed_type", value: "Type" },
    { key: "quantity", value: "Qty" },
    { key: "percentage", value: "%" },
    { key: "actions", value: "" },
  ];
</script>

<div class="page-container">
  <div class="filter-bar">
    <DatePicker
      datePickerType="range"
      on:change={(e) => {
        startDate = e.detail[0] ? new Date(e.detail[0]) : null;
        endDate = e.detail[1] ? new Date(e.detail[1]) : null;
        page = 1;
      }}
    >
      <DatePickerInput labelText="Start date" placeholder="mm/dd/yyyy" />
      <DatePickerInput labelText="End date" placeholder="mm/dd/yyyy" />
    </DatePicker>
  </div>

  {#each pagedEntries as submission}
    <Tile class="submission-tile">
      
      <div class="tile-header">
        <h4>Submission {submission.id} <span class="date">— {submission.created_at}</span></h4>
      </div>

      <div class="metrics-grid">
        <div class="metric">
          <span class="label">Temp In/Out</span>
          <span class="value">{submission.indoor_temp}° / {submission.outdoor_temp}°</span>
        </div>
        <div class="metric">
          <span class="label">Budget</span>
          <span class="value">${submission.budget}</span>
        </div>
        <div class="metric">
          <span class="label">Protein</span>
          <span class="value">{submission.protein}%</span>
        </div>
        <div class="metric">
          <span class="label">Butterfat</span>
          <span class="value">{submission.butterfat}</span>
        </div>
        <div class="metric">
          <span class="label">Water</span>
          <span class="value">{submission.water_intake} L</span>
        </div>
      </div>

      <hr class="divider" />

      <Grid narrow>
        <Row>
          <Column lg={10} md={8} sm={4}>
            <h6 class="table-title">Bovines</h6>
            <DataTable size="compact" headers={bovineHeaders} rows={submission.bovines}>
              <svelte:fragment slot="cell" let:row let:cell let:rowIndex>
                {#if editing?.submissionId === submission.id && editing.type === "bovine" && editing.index === rowIndex && cell.key !== 'id' && cell.key !== 'actions'}
                   <TextInput size="sm" bind:value={editedRow[cell.key]} />
                {:else if cell.key === "health"}
                   {#if cell.value.toLowerCase() === 'sick'}
                      <Tag type="red" size="sm">Sick</Tag>
                   {:else}
                      <Tag type="green" size="sm">Good</Tag>
                   {/if}
                {:else if cell.key === "actions"}
                   <div class="actions-cell">
                     {#if editing?.submissionId === submission.id && editing.type === "bovine" && editing.index === rowIndex}
                       <Button kind="ghost" size="small" icon={Save} iconDescription="Save" on:click={() => saveEdit(submission.id, "bovine", rowIndex)} />
                       <Button kind="ghost" size="small" icon={Close} iconDescription="Cancel" on:click={() => editing = null} />
                     {:else}
                       <Button kind="ghost" size="small" icon={Edit} iconDescription="Edit" on:click={() => startEdit(submission.id, "bovine", rowIndex)} />
                     {/if}
                   </div>
                {:else}
                   {cell.value}
                {/if}
              </svelte:fragment>
            </DataTable>
          </Column>

          <Column lg={6} md={8} sm={4}>
            <h6 class="table-title">Feeds</h6>
            <DataTable size="compact" headers={feedHeaders} rows={submission.feeds}>
              <svelte:fragment slot="cell" let:row let:cell let:rowIndex>
                 {#if editing?.submissionId === submission.id && editing.type === "feed" && editing.index === rowIndex && cell.key !== 'actions'}
                    <TextInput size="sm" bind:value={editedRow[cell.key]} />
                 {:else if cell.key === "actions"}
                    <div class="actions-cell">
                      {#if editing?.submissionId === submission.id && editing.type === "feed" && editing.index === rowIndex}
                        <Button kind="ghost" size="small" icon={Save} iconDescription="Save" on:click={() => saveEdit(submission.id, "feed", rowIndex)} />
                        <Button kind="ghost" size="small" icon={Close} iconDescription="Cancel" on:click={() => editing = null} />
                      {:else}
                        <Button kind="ghost" size="small" icon={Edit} iconDescription="Edit" on:click={() => startEdit(submission.id, "feed", rowIndex)} />
                      {/if}
                    </div>
                 {:else}
                    {cell.value || "—"}
                 {/if}
              </svelte:fragment>
            </DataTable>
          </Column>
        </Row>
      </Grid>
    </Tile>
  {/each}

  <Pagination
    totalItems={filteredEntries.length}
    pageSize={pageSize}
    page={page}
    pageSizes={[5, 10]}
    on:change={(e) => page = e.detail.page}
  />
</div>

<style>
  .page-container {
    padding: 1rem;
    max-width: 1400px; /* Prevent it from getting too wide on huge screens */
    margin: 0 auto;
  }

  .filter-bar {
    margin-bottom: 2rem;
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 4px;
  }

  /* Tile Styling */
  :global(.submission-tile) {
    margin-bottom: 2rem;
    background-color: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  .tile-header h4 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #161616;
  }
  
  .tile-header .date {
    font-weight: 400;
    color: #525252;
    font-size: 0.95rem;
  }

  /* Metrics Bar Grid */
  .metrics-grid {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }

  .metric {
    display: flex;
    flex-direction: column;
  }

  .metric .label {
    font-size: 0.75rem;
    color: #6f6f6f;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .metric .value {
    font-size: 1rem;
    font-weight: 500;
    color: #161616;
  }

  .divider {
    border: 0;
    border-top: 1px solid #e0e0e0;
    margin-bottom: 1.5rem;
  }

  .table-title {
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #525252;
    text-transform: uppercase;
    font-size: 0.75rem;
  }

  .actions-cell {
    display: flex;
    gap: 0.25rem;
  }
</style>