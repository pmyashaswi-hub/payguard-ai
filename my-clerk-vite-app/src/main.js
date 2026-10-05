import { Clerk } from "@clerk/clerk-js";

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!publishableKey) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY. Add your key to .env.local.\nRun: 1) clerk auth login  2) clerk link  3) clerk env pull — then restart the dev server.");
}

const clerk = new Clerk(publishableKey);
await clerk.load();

// Static string literals with no user input — safe to use as markup
if (clerk.user) {
  const div = document.getElementById("app");
  div.innerHTML = '<div id="user-button"></div>';
  clerk.mountUserButton(document.getElementById("user-button"));
} else {
  const div = document.getElementById("app");
  div.innerHTML = '<div id="sign-in"></div>';
  clerk.mountSignIn(document.getElementById("sign-in"));
}
