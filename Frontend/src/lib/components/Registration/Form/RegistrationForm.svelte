<script>
  import {
    Form,
    FormGroup,
    TextInput,
    PasswordInput,
    RadioButton,
    RadioButtonGroup,
    Button
  } from 'carbon-components-svelte';
  import { createEventDispatcher } from 'svelte';

  export let username = '';
  export let email = '';
  export let password = '';
  export let role = 'cow';

  let touched = false;

  const dispatch = createEventDispatcher();

  $: invalid =
    touched &&
    !/^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_\-+=\[{\]};:'",.<>/?\\|`~]{9,}$/.test(
      password
    );

  function submit(event) {
    event.preventDefault();
    touched = true;
    if (invalid) return;

    dispatch('submit', { username, email, password, role });
  }
</script>

<Form on:submit={submit}>
  <TextInput
    labelText="User name"
    placeholder="Enter user name..."
    bind:value={username}
    required
  />

  <TextInput
    labelText="Email"
    placeholder="Enter email address..."
    bind:value={email}
    type="email"
    required
  />

  <PasswordInput
    bind:value={password}
    required
    on:input={() => (touched = true)}
    labelText="Password"
    placeholder="Enter password"
    invalid={invalid}
    invalidText="Password must be at least 9 characters, include a lowercase letter and a number"
  />

  <FormGroup legendText="Role">
    <RadioButtonGroup name="role" bind:selected={role}>
      <RadioButton id="cow" value="cow" labelText="Cow Farmer" />
    </RadioButtonGroup>
  </FormGroup>

  <div class="button-container">
    <Button type="submit" kind="success">Register</Button>
  </div>
</Form>
