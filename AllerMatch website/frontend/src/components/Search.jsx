/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable jsx-a11y/alt-text */
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { callPythonFunc } from "../serverCommunication";

export default function Search(props) {
  const [sequences, setSequences] = useState("");
  const [orf, setORF] = useState("")
  const [length, setLength] = useInput({ type: "text", name: "length" });
  const [word, setWord] = useInput({ type: "text", name: "word" });
  const [cutoff, setCutoff] = useInput({ type: "text", name: "cutoff" });
  const [database, setDatabase] = useState("");
  const [propeptide, setPropeptide] = useState("");
  const [table, setTable] = useState("")

  function useInput({ type, name }) {
    const [value, setValue] = useState("");
    const input = (
      <input
        type={type}
        name={name}
        onChange={(e) => setValue(e.target.value)}
        required
      />
    );
    return [value, input];
  }

  function handleSubmit(e) {
    e.preventDefault();
    console.log('You clicked submit.');
    callPythonFunc(sequences, orf, length, word, cutoff, database, table, propeptide)
      .then((result) => {
        //Create a Blob from the PDF Stream
        const file = new Blob(
          [result.data],
          { type: 'application/pdf' });
        //Build a URL from the file
        const fileURL = URL.createObjectURL(file);
        //Open the URL on new Window
        window.open(fileURL);
        console.log("test");
        console.log(result);
      })

  }
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <br />
        <div class="row">
          <p>Sequence(s) in FASTA format</p>
          <div class="input-field col s12">
            <textarea id="textarea1" class="materialize-textarea" onChange={(e) => setSequences(e.target.value)} />
            <label for="textarea1">Sequence(s)</label>
          </div>
        </div>
        <p>Search between start and stop codons or stop and stop codons(default)</p>
        <div class="row" onChange={(e) => setORF(e.target.value)}>
          <label>
            <input name="orf" value="true" type="radio" />
            <span>Start and stop</span>
          </label>
          <label>
            <input name="orf" value="false" type="radio" />
            <span>Stop and stop</span>
          </label>
        </div>
        <p>Use if you want to search in the database with signal- and propeptide</p>
        <div class="row" onChange={(e) => setPropeptide(e.target.value)}>
          <label>
            <input name="propeptide" value="true" type="radio" />
            <span>With</span>
          </label>
          <label>
            <input name="propeptide" value="false" type="radio" />
            <span>Without</span>
          </label>
        </div>
        <div className="row">
          <div className="input-field col s4">
            <p>Sliding window minimum identity</p>
            {setCutoff}
          </div>
          <div className="input-field col s4">
            <p>Identical word length</p>
            {setWord}
          </div>
          <div className="input-field col s4">
            <p>Minimum peptide length for ORF</p>
            {setLength}
          </div>
        </div>
        <div class="row">
          <div class="col">
            Select which celiac database to use
            <select class="browser-default" onChange = {(e)=> setDatabase(e.target.value)}>
              <option value="" disabled selected>Choose your option</option>
              <option value="0">All</option>
              <option value="1">Sollid</option>
              <option value="2">ProPepper</option>
              <option value="3">AllergenOnline</option>
              <option value="4">Sollid&PP</option>
              <option value="5">Sollid&AO</option>
              <option value="6">AO&PP</option>
            </select>
          </div>
          <div class="col">
            Select which genetic code table to use
            <select class="browser-default" onChange = {(e)=> setTable(e.target.value)}>
              <option value="" disabled selected>Choose your option</option>
              <option value="1">The Standard Code</option>
              <option value="2">The Vertebrate Mitochondrial Code</option>
              <option value="3">The Yeast Mitochondrial Code</option>
              <option value="4">The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code</option>
              <option value="5">The Invertebrate Mitochondrial Code</option>
              <option value="6">The Ciliate, Dasycladacean and Hexamita Nuclear Code</option>
              <option value="9">The Echinoderm and Flatworm Mitochondrial Code</option>
              <option value="10">The Euplotid Nuclear Code</option>
              <option value="11">The Bacterial, Archaeal and Plant Plastid Code</option>
              <option value="12">The Alternative Yeast Nuclear Code</option>
              <option value="13">The Ascidian Mitochondrial Code</option>
              <option value="14">The Alternative Flatworm Mitochondrial Code</option>
              <option value="16"> Chlorophycean Mitochondrial Code</option>
              <option value="21">Trematode Mitochondrial Code</option>
              <option value="22">Scenedesmus obliquus Mitochondrial Code</option>
              <option value="23">Thraustochytrium Mitochondrial Code</option>
              <option value="24">Rhabdopleuridae Mitochondrial Code</option>
              <option value="25">Candidate Division SR1 and Gracilibacteria Code</option>
              <option value="26">Pachysolen tannophilus Nuclear Code</option>
              <option value="27">Karyorelict Nuclear Code</option>
              <option value="28">Condylostoma Nuclear Code</option>
              <option value="29">Mesodinium Nuclear Code</option>
              <option value="30">Peritrich Nuclear Code</option>
              <option value="31">Blastocrithidia Nuclear Code</option>
              <option value="33">Cephalodiscidae Mitochondrial UAA-Tyr Code</option>
            </select>
          </div>

        </div>
        {props.appState.subscription === "Basic" || props.appState.subscription === "Plus" ? <button class="waves-effect waves-light btn" type="submit">Generate PDF</button> : <div>Minimum of basic subscription needed before you can use this tool.</div>}
      </form>

    </div>
  );
}