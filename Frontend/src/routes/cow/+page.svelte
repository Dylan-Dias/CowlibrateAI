<script>
  import * as XLSX from "xlsx";
  import { goto } from "$app/navigation";
  import DashboardHeader from '$lib/components/Dashboard/UI/HeaderNav.svelte';
  import BovinesTable from '$lib/components/Dashboard/Inputs/BovinesTable.svelte';
  import FeedsTable from '$lib/components/Dashboard/Inputs/FeedsTable.svelte';
  import ConfigInputs from '$lib/components/Dashboard/Inputs/ConfigInputs.svelte';
  import Notifications from '$lib/components/Dashboard/UI/Notifications.svelte';

  let bovines = [];
  let feeds = [];
  let config = {};
  let success = false;
  let error = false;

  function addBovine() {
    bovines = [
      ...bovines,
      { id: bovines.length + 1, milk_yield: "", health: "", breed: "", lactation_stage: "", age: "" }
    ];
  }

  function addFeed() {
    feeds = [
      ...feeds,
      { feed_type: "", feed_quantity: "", feed_percentage: "" }
    ];
  }

  async function submitData() {
    success = false;
    error = false;
    const payload = {
      bovines: bovines.map(b => ({
        id: b.id,
        age: Number(b.age) || 0,
        breed: b.breed,
        health: b.health,
        milk_yield: Number(b.milk_yield) || 0,
        lactation_stage: b.lactation_stage
      })),
      feeds: feeds.map(f => ({
        feed_type: f.feed_type,
        feed_quantity: Number(f.feed_quantity) || 0,
        feed_percentage: Number(f.feed_percentage) || 0
      })),
      ...Object.fromEntries(Object.entries(config).map(([k,v]) => [k, Number(v) || null]))
    };

    try {
      const token = localStorage.getItem("token");
      const res = await fetch("https://cowlibrate.onrender.com/api/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      success = true;
      setTimeout(() => goto("/dashboard/results"), 2000);
    } catch (err) {
      console.error(err);
      error = true;
    }
  }

function normalizeHeader(header) {
  return header?.toString().trim().toLowerCase().replace(/\s+/g, "_") || "";
}

function handleFileUpload(files) {
  const file = files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const workbook = XLSX.read(new Uint8Array(e.target.result), { type: "array" });

    console.log("Available sheets:", workbook.SheetNames);

    // --- Bovines ---
    let bovineSheet = workbook.Sheets["Bovines"] || workbook.Sheets[workbook.SheetNames[0]];
    if (bovineSheet) {
      const rows = XLSX.utils.sheet_to_json(bovineSheet, { defval: "" });
      bovines = rows.map((row, i) => {
        const normalizedRow = {};
        for (let key in row) {
          normalizedRow[normalizeHeader(key)] = row[key];
        }
        return {
          id: i + 1,
          milk_yield: Number(normalizedRow.milkyield || normalizedRow.milk_yield || 0),
          health: normalizedRow.health || "",
          breed: normalizedRow.breed || "",
          lactation_stage: normalizedRow.lactationstage || normalizedRow.lactation_stage || "",
          age: Number(normalizedRow.age || 0)
        };
      });
      console.log("Parsed Bovines:", bovines);
    }

    // --- Feeds ---
    let feedSheet = workbook.Sheets["Feeds"] || workbook.Sheets[workbook.SheetNames[1]];
    if (feedSheet) {
      const rows = XLSX.utils.sheet_to_json(feedSheet, { defval: "" });
      feeds = rows.map(row => {
        const normalizedRow = {};
        for (let key in row) {
          normalizedRow[normalizeHeader(key)] = row[key];
        }
        return {
          feed_type: normalizedRow.feedtype || normalizedRow.feed_type || "",
          feed_quantity: Number(normalizedRow.feedquantity || normalizedRow.feed_quantity || 0),
          feed_percentage: Number(normalizedRow.feedpercentage || normalizedRow.feed_percentage || 0)
        };
      });
      console.log("Parsed Feeds:", feeds);
    }

    // --- Config --- 
    let configSheet = workbook.Sheets["Config"] || workbook.Sheets[workbook.SheetNames[2]];
    if (configSheet) {
      const rows = XLSX.utils.sheet_to_json(configSheet, { defval: "" });
      if (rows.length > 0) {
        const normalizedConfig = {};
        for (let key in rows[0]) {
          normalizedConfig[normalizeHeader(key)] = rows[0][key];
        }
        config = { ...config, ...normalizedConfig };
        console.log("Parsed Config:", config);
      }
    }
  };

  reader.readAsArrayBuffer(file);
}


  function logout() {
    localStorage.removeItem('token');
    goto('/register');
  }
</script>

<DashboardHeader onFileUpload={handleFileUpload} onLogout={logout} />

<main>
 

  <BovinesTable {bovines} onAddBovine={addBovine} />
  <FeedsTable {feeds} onAddFeed={addFeed} />
  <ConfigInputs bind:config />

  
  
  <div class="submit-area">
    <button on:click={submitData}>Run Optimization</button>
  </div>

  <Notifications {success} {error} />
</main>

<style>
  .submit-area {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.submit-area button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background-color: #0f62fe; /* IBM Carbon blue */
  color: #fff;
}

.submit-area button:hover {
  background-color: #0353e9;
}

.submit-area button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

</style>