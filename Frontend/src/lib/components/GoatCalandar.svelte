<script>
  import { Calendar, DayGrid, TimeGrid, List, Interaction } from "@event-calendar/core";
  import "@event-calendar/core/index.css";

  let options = $state({
    view: "dayGridMonth",
    events: [
      {
        id: 1,
        title: "Team Meeting",
        start: "2025-08-27T10:00:00",
        end: "2025-08-27T11:00:00",
        notes: "Discuss roadmap"
      },
      {
        id: 2,
        title: "Doctor Appointment",
        start: "2025-08-29T14:30:00",
        notes: "Bring reports"
      },
      {
        id: 3,
        title: "Birthday Party 🎉",
        start: "2025-09-01",
        notes: "Buy cake 🎂"
      }
    ],
    editable: true,
    selectable: true,
    headerToolbar: {
      start: "prev,next today",
      center: "title",
      end: "dayGridMonth,timeGridWeek,timeGridDay,listWeek"
    }
  });

  // Modal state
  let showModal = false;
  let selectedDate = null;
  let newTitle = "";
  let newNotes = "";

  function handleDateSelect(info) {
    selectedDate = info.startStr;
    newTitle = "";
    newNotes = "";
    showModal = true;
  }

  function saveEvent() {
    if (!newTitle) return;

    options.events = [
      ...options.events,
      {
        id: Date.now(),
        title: newTitle,
        start: selectedDate,
        notes: newNotes
      }
    ];
    showModal = false;
  }

  function handleEventClick(info) {
    const ev = info.event.extendedProps;
    alert(
      `Event: ${info.event.title}\nDate: ${info.event.start.toLocaleDateString()}\nNotes: ${ev.notes || "No notes"}`
    );
  }
</script>

<!-- Calendar -->
<Calendar
  plugins={[DayGrid, TimeGrid, List, Interaction]}
  {options}
  on:eventClick={handleEventClick}
  on:select={handleDateSelect}
/>

<!-- Modal -->
{#if showModal}
  <div class="modal-backdrop">
    <div class="modal">
      <h2>Add Event</h2>
      <label>
        Title:
        <input type="text" bind:value={newTitle} />
      </label>
      <label>
        Notes:
        <textarea rows="3" bind:value={newNotes}></textarea>
      </label>
      <div class="actions">
        <button on:click={saveEvent}>Save</button>
        <button on:click={() => (showModal = false)}>Cancel</button>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .modal {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    width: 300px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
  }

  .modal h2 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
  }

  label {
    display: block;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }

  input,
  textarea {
    width: 100%;
    margin-top: 0.3rem;
    padding: 0.4rem;
    border: 1px solid #ccc;
    border-radius: 6px;
  }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
  }

  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  button:first-child {
    background: #4caf50;
    color: white;
  }

  button:last-child {
    background: #ccc;
  }
</style>
