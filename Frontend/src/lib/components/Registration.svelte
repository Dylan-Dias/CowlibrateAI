<script>
  import 'carbon-components-svelte/css/g10.css';
  import { goto } from '$app/navigation';
  import {
    TextInput,
    PasswordInput,
    Form,
    FormGroup,
    RadioButton,
    RadioButtonGroup,
    Button,
  } from "carbon-components-svelte";

  let username = "";
  let email = "";
  let password = "";
  let role = "goat";
  let invalid = false;
  let touched = false;

  // Reactive password validation only after user starts typing
  $: invalid = touched && !/^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{6,}$/.test(password);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!username || !email || !password) {
      alert("Please fill out all fields.");
      return;
    }

    touched = true;
    if (invalid) {
      alert("Please enter a valid password.");
      return;
    }

    const response = await fetch("http://localhost:8080/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role })
    });

    if (response.ok) {
      // Redirect based on role to the correct dashboard page
      const dashboardMap = {
        goat: "/dashboard/GoatAnalytics",
        cow: "/dashboard/CowAnalytics"
      };
      goto(dashboardMap[role] || "/dashboard");
    } else {
      const msg = await response.text();
      alert("Registration failed: " + msg);
    }
  }
</script>

<main>
  <h1>Cowlibrate AI Registration</h1>

  <Form on:submit={handleSubmit}>
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
      type="password"
      labelText="Password"
      placeholder="Enter password"
      invalid={invalid}
      invalidText="Password must be at least 6 characters, include a lowercase letter and a number"
    />

    <FormGroup legendText="Role">
      <RadioButtonGroup name="role" bind:selected={role}>
        <RadioButton id="radio-2" value="cow" labelText="Cow Farmer" />
      </RadioButtonGroup>
    </FormGroup>

    <div class="button-container">
      <Button type="submit" kind="success" class="submit-button">
        Register
      </Button>
    </div>
  </Form>
</main>

<style>
  main {
    max-width: 640px;
    margin: 4rem auto;
    padding: 2.5rem;
    background-color: var(--cds-layer);
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  }

  h1 {
    text-align: center;
    font-size: 2rem;
    color: var(--cds-text-primary);
    margin-bottom: 2rem;
  }

  :global(.bx--form-item) {
    margin-bottom: 1.5rem;
  }

  :global(.bx--form-item .bx--label) {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--cds-text-secondary);
  }

  :global(.bx--text-input),
  :global(.bx--password-input) {
    font-size: 1rem;
    background-color: var(--cds-layer);
  }

  :global(.bx--text-input:focus),
  :global(.bx--password-input:focus),
  :global(.bx--radio-button:focus) {
    outline: 2px solid #42be65 !important;
    box-shadow: 0 0 0 2px rgba(66, 190, 101, 0.3);
    border-color: #42be65;
  }

  :global(.bx--form-group) {
    padding-top: 1rem;
    margin-top: 2rem;
    border-top: 1px solid var(--cds-border-subtle);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  :global(.bx--radio-button-group) {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
  }

  .button-container {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }

  @media (max-width: 600px) {
    main {
      padding: 1.5rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    :global(.bx--radio-button-group) {
      flex-direction: column;
      align-items: center;
    }

    .button-container {
      width: 100%;
    }

    :global(.bx--btn) {
      width: 100%;
    }
  }
</style>
