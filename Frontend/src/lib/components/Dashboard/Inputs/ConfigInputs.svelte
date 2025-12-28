<script>
  import { NumberInput } from "carbon-components-svelte";
 
export let config = {
  indoor_temp: 20,
  outdoor_temp: 15,
  water_intake: 30,
  budget: 1000,
  protein: 3.2,
  butterfat: 4.0,
  somatic_cell_count: 200
};



</script>

<h2>Additional Inputs</h2>
<div class="grid-row">
  <NumberInput label="Indoor Temp (°C)" bind:value={config.indoor_temp} invalid={false}/>
  <NumberInput label="Outdoor Temp (°C)" bind:value={config.outdoor_temp} invalid={false} />
  <NumberInput label="Budget ($)" min="0" bind:value={config.budget} invalid={false} />
</div>
<div class="grid-row">
  <NumberInput label="Protein (%)" min="0" bind:value={config.protein} invalid={false} />
  <NumberInput label="Butterfat (%)" min="0" bind:value={config.butterfat} invalid={false} />
  <NumberInput label="Somatic Cell Count" min="0" bind:value={config.somatic_cell_count} invalid={false}  />
  <NumberInput label="Water Intake (L/day)" min="0" bind:value={config.water_intake} invalid={false} />
</div>
