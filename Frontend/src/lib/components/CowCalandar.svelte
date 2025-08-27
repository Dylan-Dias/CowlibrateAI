<script>
  import { onMount } from 'svelte';
  import { Calendar, DayGrid, TimeGrid, List, Interaction } from '@event-calendar/core';
  import '@event-calendar/core/index.css';

  // Reactive state for the calendar options
  let options = $state({
    view: 'dayGridMonth', // default view
    events: [
      { id: 1, title: 'Team Meeting', start: '2025-08-27T10:00:00', end: '2025-08-27T11:00:00' },
      { id: 2, title: 'Doctor Appointment', start: '2025-08-29T14:30:00' },
      { id: 3, title: 'Birthday Party 🎉', start: '2025-09-01' }
    ],
    editable: true,   // allow drag/drop & resize
    selectable: true, // allow selecting slots
    headerToolbar: {
      start: 'prev,next today',
      center: 'title',
      end: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    }
  });

  // Optional: event handlers
  function handleEventClick(info) {
    alert(`Event clicked: ${info.event.title}`);
  }

  function handleDateSelect(info) {
    const title = prompt('Enter a new event title:');
    if (title) {
      options.events = [
        ...options.events,
        { id: Date.now(), title, start: info.startStr, end: info.endStr }
      ];
    }
  }
</script>

<Calendar
  plugins={[DayGrid, TimeGrid, List, Interaction]}
  {options}
  on:eventClick={handleEventClick}
  on:select={handleDateSelect}
/>
