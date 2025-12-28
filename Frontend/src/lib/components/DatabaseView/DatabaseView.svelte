<script>
  import {
    TableContainer, Table, TableHead, TableHeader,
    TableBody, TableRow, TableCell, Button, TextInput
  } from "carbon-components-svelte";

  export let entries = [];
  let editing = null;
  let editedRow = {};

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
</script>

<style>
  .submission-card {
    padding: 1.5rem;
    margin-bottom: 2rem;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  .section-title {
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    font-size: 1.25rem;
    font-weight: 600;
    color: #1d1d1d;
  }

  .submission-header {
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 0.5rem;
  }

  .details-grid {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    grid-gap: 0.5rem 1.2rem;
    background: #fafafa;
    padding: 1rem;
    border-radius: 6px;
    border: 1px solid #eee;
  }

  .detail-item {
    font-size: 0.95rem;
    line-height: 1.4;
  }
</style>

{#each entries as submission}
  <div class="submission-card">
    <div class="submission-header">
      Submission {submission.id} — {submission.created_at}
    </div>

    <!-- 🐄 BOVINES TABLE -->
    <div class="section-title">Bovines</div>

    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeader>ID</TableHeader>
            <TableHeader>Milk Yield</TableHeader>
            <TableHeader>Health</TableHeader>
            <TableHeader>Breed</TableHeader>
            <TableHeader>Lactation Stage</TableHeader>
            <TableHeader>Age</TableHeader>
            <TableHeader>Actions</TableHeader>
          </TableRow>
        </TableHead>

        <TableBody>
          {#each submission.bovines as cow, i}
            <TableRow>
              {#if editing && editing.submissionId === submission.id && editing.type === "bovine" && editing.index === i}
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

    <!-- 🌾 FEEDS TABLE -->
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
              {#if editing && editing.submissionId === submission.id && editing.type === "feed" && editing.index === i}
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

    <!-- 🔍 DETAILS SECTION -->
    <div class="section-title">Submission Details</div>
    <div class="details-grid">
      <div class="detail-item">Indoor Temp (°C): <strong>{submission.indoor_temp}</strong></div>
      <div class="detail-item">Outdoor Temp (°C): <strong>{submission.outdoor_temp}</strong></div>
      <div class="detail-item">Budget ($): <strong>{submission.budget}</strong></div>
      <div class="detail-item">Protein (%): <strong>{submission.protein}</strong></div>
      <div class="detail-item">Butterfat (%): <strong>{submission.butterfat}</strong></div>
      <div class="detail-item">Somatic Cell Count: <strong>{submission.somatic_cell_count}</strong></div>
      <div class="detail-item">Water Intake (L/day): <strong>{submission.water_intake}</strong></div>
    </div>

  </div>
{/each}
