"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[738],{7830:()=>{const e=["Escape"],t=["ArrowLeft"],s=["ArrowRight"];let n=null,i=null;async function r(){!function(){const e=document.getElementsByClassName("file-extended-open");for(const t of e)t.addEventListener("click",c)}(),function(){const e=document.getElementsByClassName("file-extended-close");for(const t of e)t.addEventListener("click",l)}(),document.addEventListener("keydown",(function(n){if(e.includes(n.key)){const e=document.querySelector(".file-extended:target .file-extended-close a");e&&e.click()}else if(t.includes(n.key)){const e=document.querySelector(".file-extended:target .file-extended-previous a");e&&e.click()}else if(s.includes(n.key)){const e=document.querySelector(".file-extended:target .file-extended-next a");e&&e.click()}}))}function c(){n=window.scrollX,i=window.scrollY}function l(e){window.location="#",window.scrollTo({left:n,top:i}),n=null,i=null,e.preventDefault()}class o{hideSearchKeys=["Escape"];nextResultKeys=["ArrowDown"];previousResultKeys=["ArrowUp"];index=null;constructor(){this.search=document.getElementById("search"),this.form=this.search.getElementsByTagName("form").item(0),this.queryElement=document.getElementById("search-query"),this.resultsContainer=document.getElementById("search-results-container"),this.documentY=null}initialize(){this.form.addEventListener("submit",(e=>{e.preventDefault(),e.stopPropagation()})),this.queryElement.addEventListener("keyup",(()=>{(async()=>{await this.perform(this.queryElement.value)})()})),this.queryElement.addEventListener("keydown",(e=>{this.navigateResults(e.key)})),this.resultsContainer.addEventListener("keydown",(e=>{this.navigateResults(e.key)})),this.queryElement.addEventListener("focus",(()=>{this.showSearchResults()})),this.search.getElementsByClassName("overlay-close")[0].addEventListener("mouseup",(()=>{this.hideSearchResults()})),document.addEventListener("keydown",(e=>{this.hideSearchKeys.includes(e.key)&&this.hideSearchResults()}))}navigateResults(e){if(this.previousResultKeys.includes(e)){if(document.activeElement===this.queryElement)return;if(document.activeElement.classList.contains("search-result-target")){const e=document.activeElement.closest(".search-result").previousElementSibling;if(e){const t=e.querySelector(".search-result-target");return void(t&&t.focus())}this.queryElement.focus()}}else if(this.nextResultKeys.includes(e)){if(document.activeElement===this.queryElement){const e=this.resultsContainer.getElementsByClassName("search-result-target");return void(e.length&&e[0].focus())}if(document.activeElement.classList.contains("search-result-target")){const e=document.activeElement.closest(".search-result").nextElementSibling;if(e){const t=e.querySelector(".search-result-target");t&&t.focus()}}}}setSearchEntries(e){this.resultsContainer.innerHTML=this.renderResults(e),this.resultsContainer.scrollTop=0}showSearchResults(){this.documentY||(this.documentY=window.scrollY),this.search.classList.add("overlay"),document.body.classList.add("has-overlay"),this.search.contains(document.activeElement)||this.queryElement.focus()}hideSearchResults(){const e=document.activeElement;this.search.contains(e)&&e.blur(),this.search.classList.remove("overlay"),document.body.classList.remove("has-overlay"),this.documentY&&(window.scrollTo({top:this.documentY}),this.documentY=null)}async getIndex(){if(null===this.index){const e=await fetch(this.search.dataset.bettySearchIndex);this.index=await e.json()}return this.index}async perform(e){const t=await this.getIndex();this.setSearchEntries(t.index.filter((t=>this.match(e,t.text))))}match(e,t){const s=e.toLowerCase().split(/\s/);for(const e of s)if(!t.includes(e))return!1;return!0}renderResults(e){return this.index.resultsContainerTemplate.replace("{{{ betty-search-results }}}",e.map((e=>this.renderResult(e))).join(""))}renderResult(e){return this.index.resultContainerTemplate.replace("{{{ betty-search-result }}}",e.result)}}async function a(){const e=document.getElementsByClassName("show-toggle");for(const t of e)u(t)}function u(e){e.addEventListener("click",(e=>{const t=d(e.target);t&&t.classList.toggle("show-shown")}))}function d(e){const t=e.parentNode;if(t)return t.classList.contains("show")?t:d(t)}!async function(){await Promise.allSettled([r(),a()]),(new o).initialize()}()}},e=>{var t;t=7830,e(e.s=t)}]);