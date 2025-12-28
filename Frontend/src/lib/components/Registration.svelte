<script>
  import 'carbon-components-svelte/css/g10.css';
    import '../styles/Registration.css';
  import { goto } from '$app/navigation';

 import { register } from "$lib/services/auth";
  import { InlineNotification, Form, FormGroup, TextInput, PasswordInput, RadioButton, RadioButtonGroup, Button } from "carbon-components-svelte";

  let username = "";
  let email = "";
  let password = "";
  let role = "cow";
  let touched = false;
  let error = "";
  let success = "";

  $: invalid = touched && !/^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_\-+=\[{\]};:'",.<>/?\\|`~]{9,}$/.test(password);

  async function handleSubmit(event) {
    event.preventDefault();
    touched = true;

    if (invalid) return;

    try {
      const data = await register(username, email, password, role.toLowerCase());
      success = "Registration successful! Redirecting...";
      error = "";

      // Immediately route based on role
      setTimeout(() => {
      if (data.user?.role === "goat") {
        goto("/dashboard/GoatAnalytics");
      } else if (data.user?.role === "cow") {
        goto("/cow");
      } else {
        goto("/dashboard");
      }
       }, 1500);
    } catch (err) {
      error = err.message;
      success = "";
    }
  }
</script>

<main>
  <h1>Registration</h1>

  {#if error}
    <InlineNotification title="Error" subtitle={error} kind="error" />
  {/if}

  {#if success}
    <InlineNotification title="Success" subtitle={success} kind="success" />
  {/if}

  <Form on:submit={handleSubmit}>
    <TextInput labelText="User name" placeholder="Enter user name..." bind:value={username} required />
    <TextInput labelText="Email" placeholder="Enter email address..." bind:value={email} type="email" required />

    <PasswordInput
      bind:value={password}
      required
      on:input={() => (touched = true)}
      type="password"
      labelText="Password"
      placeholder="Enter password"
      invalid={invalid}
      invalidText="Password must be at least 9 characters, include a lowercase letter and a number"
    />

    <FormGroup legendText="Role">
      <RadioButtonGroup name="role" bind:selected={role}>
        <RadioButton id="radio-2" value="cow" labelText="Cow Farmer" />
      </RadioButtonGroup>
    </FormGroup>

    <div class="button-container">
      <Button type="submit" kind="success">Register</Button>
    </div>
  </Form>
</main>
