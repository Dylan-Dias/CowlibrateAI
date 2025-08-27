<script>
  import 'carbon-components-svelte/css/g10.css';
  import { goto } from '$app/navigation';
  import '../styles/Registration.css';
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
  let role = "cow"; // default lowercase to match dashboardMap
  let touched = false;

  // Reactive password validation
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

    const response = await fetch("http://localhost:8080/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role: role.toLowerCase() })
    });

    if (response.ok) {
      const dashboardMap = {
        goat: "/dashboard/GoatAnalytics",
        cow: "/dashboard/CowAnalytics"
      };
      goto(dashboardMap[role.toLowerCase()] || "/dashboard");
    } else {
      const data = await response.json();
      alert("Registration failed: " + (data.detail || data.message));
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
        <RadioButton id="radio-3" value="goat" labelText="Goat Farmer" />

      </RadioButtonGroup>
    </FormGroup>

    <div class="button-container">
      <Button type="submit" kind="success" class="submit-button">
        Register
      </Button>
    </div>
  </Form>
</main>

