<script>
  import {
    TableContainer, Table, TableHead, TableHeader,
    TableBody, TableRow, TableCell,
    Button, TextInput,
    Pagination,
    DatePicker, DatePickerInput
  } from "carbon-components-svelte";

  export let entries = [];

  /* Editing */
  let editing = null;
  let editedRow = {};

  /* Pagination */
  let pageSize = 5;
  let page = 1;

  /* Date filtering */
  let startDate = null;
  let endDate = null;

  /* ------------------ Editing ------------------ */
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

  /* ------------------ Filters ------------------ */
  $: filteredEntries = entries.filter(e => {
    if (!startDate && !endDate) return true;
    const created = new Date(e.created_at);
    if (startDate && created < startDate) return false;
    if (endDate && created > endDate) return false;
    return true;
  });

  /* ------------------ Pagination ------------------ */
  $: pagedEntries = filteredEntries.slice(
    (page - 1) * pageSize,
    page * pageSize
  );
</script>

<!--  DATE FILTER -->
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

<!--  SUBMISSIONS -->
{#each pagedEntries as submission}
  <div class="submission-card">
    <div class="submission-header">
      Submission {submission.id} — {submission.created_at}
    </div>

    <!--  BOVINES -->
    <div class="section-title">Bovines</div>
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>ID</TableHeader>
            <TableHeader>Milk Yield</TableHeader>
            <TableHeader>Health</TableHeader>
            <TableHeader>Breed</TableHeader>
            <TableHeader>Lactation</TableHeader>
            <TableHeader>Age</TableHeader>
            <TableHeader>Actions</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {#each submission.bovines as cow, i}
            <TableRow>
              {#if editing?.submissionId === submission.id && editing.type === "bovine" && editing.index === i}
                <TableCell>{cow.id}</TableCell>
                <TableCell><TextInput bind:value={editedRow.milk_yield} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.health} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.breed} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.lactation_stage} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.age} size="sm" /></TableCell>
                <TableCell>
                  <Button size="sm" on:click={() => saveEdit(submission.id, "bovine", i)}>Save</Button>
                  <Button size="sm" kind="secondary" on:click={() => editing = null}>Cancel</Button>
                </TableCell>
              {:else}
                <TableCell>{cow.id}</TableCell>
                <TableCell>{cow.milk_yield}</TableCell>
                <TableCell>{cow.health}</TableCell>
                <TableCell>{cow.breed}</TableCell>
                <TableCell>{cow.lactation_stage}</TableCell>
                <TableCell>{cow.age}</TableCell>
                <TableCell>
                  <Button size="sm" on:click={() => startEdit(submission.id, "bovine", i)}>Edit</Button>
                </TableCell>
              {/if}
            </TableRow>
          {/each}
        </TableBody>
      </Table>
    </TableContainer>

    <!--  FEEDS -->
    <div class="section-title">Feeds</div>
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>Feed Type</TableHeader>
            <TableHeader>Quantity</TableHeader>
            <TableHeader>Percentage</TableHeader>
            <TableHeader>Actions</TableHeader>
          </TableRow>
        </TableHead>
        <TableBody>
          {#each submission.feeds as feed, i}
            <TableRow>
              {#if editing?.submissionId === submission.id && editing.type === "feed" && editing.index === i}
                <TableCell><TextInput bind:value={editedRow.feed_type} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.quantity} size="sm" /></TableCell>
                <TableCell><TextInput bind:value={editedRow.percentage} size="sm" /></TableCell>
                <TableCell>
                  <Button size="sm" on:click={() => saveEdit(submission.id, "feed", i)}>Save</Button>
                  <Button size="sm" kind="secondary" on:click={() => editing = null}>Cancel</Button>
                </TableCell>
              {:else}
                <TableCell>{feed.feed_type}</TableCell>
                <TableCell>{feed.quantity}</TableCell>
                <TableCell>{feed.percentage}</TableCell>
                <TableCell>
                  <Button size="sm" on:click={() => startEdit(submission.id, "feed", i)}>Edit</Button>
                </TableCell>
              {/if}
            </TableRow>
          {/each}
        </TableBody>
      </Table>
    </TableContainer>

    <!--  DETAILS -->
    <div class="section-title">Submission Details</div>
    <TableContainer>
      <Table size="sm">
        <TableBody>
          <TableRow><TableCell>Indoor Temp</TableCell><TableCell>{submission.indoor_temp}</TableCell></TableRow>
          <TableRow><TableCell>Outdoor Temp</TableCell><TableCell>{submission.outdoor_temp}</TableCell></TableRow>
          <TableRow><TableCell>Budget ($)</TableCell><TableCell>{submission.budget}</TableCell></TableRow>
          <TableRow><TableCell>Protein (%)</TableCell><TableCell>{submission.protein}</TableCell></TableRow>
          <TableRow><TableCell>Butterfat (%)</TableCell><TableCell>{submission.butterfat}</TableCell></TableRow>
          <TableRow><TableCell>SCC</TableCell><TableCell>{submission.somatic_cell_count}</TableCell></TableRow>
          <TableRow><TableCell>Water Intake</TableCell><TableCell>{submission.water_intake}</TableCell></TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  </div>
{/each}

<!--  PAGINATION -->
<Pagination
  totalItems={filteredEntries.length}
  pageSize={pageSize}
  page={page}
  pageSizes={[5]}
  on:change={(e) => page = e.detail.page}
/>

<style>
  .submission-card {
    padding: 1.25rem;
    margin-bottom: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }

  .submission-header {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  .section-title {
    margin: 1.25rem 0 0.5rem;
    font-weight: 600;
  }
</style>
