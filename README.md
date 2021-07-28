# Allermatch revamp
This repository contains all the files used in the Allermatch website revamp.

## Changes

- Different layout
- Added user account
- Added subscription tiers
- Added more information about the tool
- Connected the updated Python tool to the website
- Added the ability to store previous searches

## How to add a page
Create a new file in Components in the frontend folder. For this example we're going to add CutePets.jsx. Within the new file the first thing to add is this piece of code(rename parts named CutePets with your page name!)
```javascript
import React from "react";
export default function CutePets(props) {
    // here you can add javascript code
  return (
    <div>
    This is a HTML area for this page, using normal HTML you can add to this page as you please. For more in depth functionality like using buttons/forms/display text from variables, please look up React tutorials.
    </div>
  );
}
```

After this, you need to go to App.jsx and add a route to the newly created page. First you need to import your newly created page, this needs to be placed at the same place as all the other imports.
```javascript
import cutePets from "./components/CutePets";
```
Lets say you want to add a button to the side menu so you can navigate to CutePets. Just above the <Switch> you can add a <Link> to your page like this.
```javascript
<Link to="/cutepets">
    <li>
        <a><i class="material-icons" id="cutepets">business</i>Cute Pets</a>
    </li>
</Link>
```
After this, you only have to add your new <Link> to your <Switch>. You can just add this right after the last </Route> closing tag but before the </Switch> closing tag.
```javascript
<Route path="/cutepets">
    {this.state.logged_in ? <CutePets /> : <Home />}
</Route>
```

After this your page should be added. You can now edit your HTML and Javascript blocks in CutePets.jsx!
