"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[646],{7395:(e,t,a)=>{var o=a(165),n=a(5111),s=a.n(n);async function l(){const e=document.getElementsByClassName("tree");await Promise.allSettled(Array.from(e).map((e=>async function(e,t){const a=await fetch(e.dataset.bettyPeople),n=await a.json(),s={nodes:[],edges:[]},l=n[t];r(l,s.nodes),c(l,s,n),d(l,s,n);const i=(0,o.A)({container:document.getElementsByClassName("tree")[0],layout:{name:"dagre"},wheelSensitivity:.25,style:[{selector:"node",style:{content:"data(label)",shape:"round-rectangle","text-valign":"center","text-halign":"center","background-color":"#eee",width:"label",height:"label",padding:"9px"}},{selector:"node.public",style:{color:"#149988"}},{selector:"node.public.hover",style:{color:"#2a615a"}},{selector:"edge",style:{"curve-style":"taxi","taxi-direction":"downward",width:4,"target-arrow-shape":"triangle","line-color":"#777","target-arrow-color":"#777"}}],elements:s});i.zoom({level:1,position:i.getElementById(t).position()}),i.on("mouseover","node.public",(e=>{e.target.addClass("hover")})),i.on("mouseout","node.public",(e=>{e.target.removeClass("hover")})),i.on("tap","node.public",(e=>{window.location=e.target.data().url}))}(e,e.dataset.bettyPersonId))))}function r(e,t){t.push({data:{id:e.id,label:e.label,url:e.url},selectable:!1,grabbable:!1,pannable:!0,classes:e.private?[]:["public"]})}function c(e,t,a){for(const o of e.parentIds){const n=a[o];t.edges.push({data:{source:n.id,target:e.id}}),r(n,t.nodes),c(n,t,a)}}function d(e,t,a){for(const o of e.childIds){const n=a[o];t.edges.push({data:{source:e.id,target:n.id}}),r(n,t.nodes),d(n,t,a)}}o.A.use(s()),async function(){await l()}()}},e=>{e.O(0,[111,165],(()=>{return t=7395,e(e.s=t);var t}));e.O()}]);