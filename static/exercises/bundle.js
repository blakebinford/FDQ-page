"use strict";

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function ownKeys(e, r) { var t = Object.keys(e); if (Object.getOwnPropertySymbols) { var o = Object.getOwnPropertySymbols(e); r && (o = o.filter(function (r) { return Object.getOwnPropertyDescriptor(e, r).enumerable; })), t.push.apply(t, o); } return t; }
function _objectSpread(e) { for (var r = 1; r < arguments.length; r++) { var t = null != arguments[r] ? arguments[r] : {}; r % 2 ? ownKeys(Object(t), !0).forEach(function (r) { _defineProperty(e, r, t[r]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(t)) : ownKeys(Object(t)).forEach(function (r) { Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(t, r)); }); } return e; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t["return"] && (u = t["return"](), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
var _React = React,
  useState = _React.useState,
  useRef = _React.useRef,
  useEffect = _React.useEffect;

// Inject hover-tooltip CSS once
(function () {
  if (document.getElementById('fdq-tooltip-style')) return;
  var s = document.createElement('style');
  s.id = 'fdq-tooltip-style';
  s.textContent = "\n    .tip-wrap { position: relative; display: inline-flex; align-items: center; }\n    .tip-icon {\n      display: inline-flex; align-items: center; justify-content: center;\n      width: 13px; height: 13px; border-radius: 50%;\n      background: #1a3040; border: 1px solid #3a5a6a;\n      color: #7a9db0; font-size: 8px; font-weight: 700;\n      cursor: default; flex-shrink: 0; margin-left: 5px;\n      font-style: normal; line-height: 1; font-family: 'IBM Plex Mono', monospace;\n      user-select: none;\n    }\n    .tip-icon:hover { background: #243a48; border-color: #7a9db0; color: #a0c4d4; }\n    .tip-box {\n      display: none;\n      position: absolute;\n      bottom: calc(100% + 6px);\n      left: 50%; transform: translateX(-50%);\n      min-width: 220px; max-width: 280px;\n      background: #1a2a34;\n      border: 1px solid #3a5a6a;\n      border-left: 2px solid #7a9db0;\n      padding: 6px 9px;\n      font-size: 7.5px; color: #a0c4d4;\n      line-height: 1.6; font-style: italic;\n      font-family: 'IBM Plex Mono', monospace;\n      z-index: 200; pointer-events: none;\n      white-space: normal; word-break: break-word;\n    }\n    .tip-box::after {\n      content: ''; position: absolute; top: 100%; left: 50%;\n      transform: translateX(-50%);\n      border: 5px solid transparent;\n      border-top-color: #3a5a6a;\n    }\n    .tip-wrap:hover .tip-box { display: block; }\n  ";
  document.head.appendChild(s);
})();
(function () {
  if (document.getElementById('fdq-input-style')) return;
  var s = document.createElement('style');
  s.id = 'fdq-input-style';
  s.textContent = [
    '.fdq-form-input::placeholder {',
    '  color: #52a366;',
    '  font-style: italic;',
    '  font-size: 9px;',
    '  opacity: 0.7;',
    '}',
    '.fdq-form-input:focus { outline: none; }',
    '.fdq-form-input-wrap {',
    '  outline: 1px solid #2a4a2a;',
    '  background: rgba(42,74,42,0.06);',
    '  border-left: 2px solid #3a6a3a;',
    '}',
    '.fdq-form-input-wrap:focus-within {',
    '  outline: 1px solid #52a366 !important;',
    '  background: rgba(42,74,42,0.14) !important;',
    '  border-left-color: #52a366 !important;',
    '}',
    '.fdq-form-input {',
    '  caret-color: #52a366;',
    '}'
  ].join("\n");
  document.head.appendChild(s);
})();
var SCENARIO = {
  project: "Mustang Creek Compressor Station",
  system: "Discharge Piping — Train A",
  spec: "Q-SPEC-2200 Rev. 3",
  procedure: "ASME B16.5 Class 600 / TQ-44A",
  service: "Natural Gas — Sour Service",
  gasketLot: "GT-2241",
  inspector: "J. Reed",
  joints: [{
    id: "FLG-001",
    location: "Suction Nozzle N1",
    size: '6"',
    target: 185,
    pattern: "Cross",
    passes: 3
  }, {
    id: "FLG-002",
    location: "Discharge Nozzle N2",
    size: '6"',
    target: 185,
    pattern: "Cross",
    passes: 3
  }, {
    id: "FLG-003",
    location: "Recycle Line Tie-In",
    size: '4"',
    target: 120,
    pattern: "Cross",
    passes: 3
  }, {
    id: "FLG-004",
    location: "PSV-101 Inlet",
    size: '3"',
    target: 120,
    pattern: "Cross",
    passes: 3
  }, {
    id: "FLG-005",
    location: "Drain Connection",
    size: '1.5"',
    target: 65,
    pattern: "Cross",
    passes: 2
  }]
};
var ANSWERS = {
  "FLG-001": {
    achieved: "185",
    pattern: "Cross",
    passes: "3",
    gasket: "GT-2241",
    initials: "J. REED",
    result: "ACC"
  },
  "FLG-002": {
    achieved: "185",
    pattern: "Cross",
    passes: "3",
    gasket: "GT-2241",
    initials: "J. REED",
    result: "ACC"
  },
  "FLG-003": {
    achieved: "120",
    pattern: "Cross",
    passes: "3",
    gasket: "GT-2241",
    initials: "J. REED",
    result: "ACC"
  },
  "FLG-004": {
    achieved: "120",
    pattern: "Cross",
    passes: "3",
    gasket: "GT-2241",
    initials: "J. REED",
    result: "ACC"
  },
  "FLG-005": {
    achieved: "65",
    pattern: "Cross",
    passes: "2",
    gasket: "GT-2241",
    initials: "J. REED",
    result: "ACC"
  }
};
var COLS = [{
  key: "achieved",
  label: "Achieved\nTorque (ft-lb)",
  hint: "e.g. 185"
}, {
  key: "pattern",
  label: "Bolt\nPattern",
  hint: "e.g. Cross"
}, {
  key: "passes",
  label: "# of\nPasses",
  hint: "e.g. 3"
}, {
  key: "gasket",
  label: "Gasket\nLot #",
  hint: "e.g. GT-2241"
}, {
  key: "initials",
  label: "Inspector\nInitials",
  hint: "J. REED"
}, {
  key: "result",
  label: "Result\nACC/REJ",
  hint: "ACC or REJ"
}];
var BOM = [{
  item: "1",
  qty: "2",
  description: '6" 600# WN Flange RF, ASME B16.5',
  material: "ASTM A105N",
  certNo: "MTR-6612"
}, {
  item: "2",
  qty: "1",
  description: '4" 600# WN Flange RF, ASME B16.5',
  material: "ASTM A105N",
  certNo: "MTR-6612"
}, {
  item: "3",
  qty: "1",
  description: '3" 600# WN Flange RF, ASME B16.5',
  material: "ASTM A105N",
  certNo: "MTR-6613"
}, {
  item: "4",
  qty: "1",
  description: '1.5" 600# WN Flange RF, ASME B16.5',
  material: "ASTM A105N",
  certNo: "MTR-6613"
}, {
  item: "5",
  qty: "5",
  description: 'SWG 316SS/Flex Graphite, ASME B16.20',
  material: "316SS/Flex Graphite",
  certNo: "GT-2241"
}, {
  item: "6",
  qty: "32",
  description: 'Stud Bolt 1"×7.25" (6" 600#)',
  material: "ASTM A193 B7",
  certNo: "MTR-8801"
}, {
  item: "7",
  qty: "16",
  description: 'Stud Bolt 7/8"×6.25" (4" 600#)',
  material: "ASTM A193 B7",
  certNo: "MTR-8801"
}, {
  item: "8",
  qty: "12",
  description: 'Stud Bolt 3/4"×5.75" (3" 600#)',
  material: "ASTM A193 B7",
  certNo: "MTR-8801"
}, {
  item: "9",
  qty: "8",
  description: 'Stud Bolt 5/8"×4.50" (1.5" 600#)',
  material: "ASTM A193 B7",
  certNo: "MTR-8801"
}, {
  item: "10",
  qty: "64",
  description: 'Heavy Hex Nut (all sizes)',
  material: "ASTM A194 2H",
  certNo: "MTR-8802"
}];
var TORQUE_SPEC = [{
  size: '6"',
  boltQty: "16",
  boltSize: '1" × 7.25"',
  snug: "65",
  mid: "130",
  "final": "185",
  passes: "3"
}, {
  size: '4"',
  boltQty: "16",
  boltSize: '7/8" × 6.25"',
  snug: "40",
  mid: "80",
  "final": "120",
  passes: "3"
}, {
  size: '3"',
  boltQty: "12",
  boltSize: '3/4" × 5.75"',
  snug: "40",
  mid: "80",
  "final": "120",
  passes: "3"
}, {
  size: '1.5"',
  boltQty: "8",
  boltSize: '5/8" × 4.50"',
  snug: "20",
  mid: "45",
  "final": "65",
  passes: "2"
}];

// Per-joint torque forms — field data the inspector recorded
var JOINT_FORMS = {
  "FLG-001": {
    id: "FLG-001",
    location: "Suction Nozzle N1",
    size: '6"',
    cls: "600#",
    boltSize: '1" dia × 7.25" L',
    boltQty: "16",
    boltMat: "ASTM A193 B7",
    boltHeat: "HT-9042",
    boltCert: "MTR-8801",
    nutMat: "ASTM A194 2H",
    nutHeat: "HT-9043",
    nutCert: "MTR-8802",
    gasketType: "Spiral Wound 316SS/Flex Graphite",
    gasketStd: "ASME B16.20",
    gasketLot: "GT-2241",
    flangeMat: "ASTM A105N",
    flangeHeat: "HT-3821A",
    flangeCert: "MTR-6612",
    lubricant: "Molykote® G-1000 PTFE Thread Paste",
    targetTorque: "185",
    achievedTorque: "185",
    snugTorque: "65",
    midTorque: "130",
    finalTorque: "185",
    pattern: "Cross (Star)",
    passes: "3",
    alignmentCheck: "PASS",
    gasketCondition: "Good — no scoring or damage",
    boltEngagement: "Full thread engagement verified all 16 bolts",
    surfaceFinish: "125–250 AARH verified both flanges",
    date: "03/14/2026",
    shift: "Day",
    wrenchId: "TW-104",
    wrenchCalDue: "06/01/2026",
    inspector: "J. Reed",
    initials: "J. REED",
    result: "ACC",
    remarks: "All bolts torqued per TQ-44A. Cross pattern maintained. No leaks. Gasket seated properly."
  },
  "FLG-002": {
    id: "FLG-002",
    location: "Discharge Nozzle N2",
    size: '6"',
    cls: "600#",
    boltSize: '1" dia × 7.25" L',
    boltQty: "16",
    boltMat: "ASTM A193 B7",
    boltHeat: "HT-9042",
    boltCert: "MTR-8801",
    nutMat: "ASTM A194 2H",
    nutHeat: "HT-9043",
    nutCert: "MTR-8802",
    gasketType: "Spiral Wound 316SS/Flex Graphite",
    gasketStd: "ASME B16.20",
    gasketLot: "GT-2241",
    flangeMat: "ASTM A105N",
    flangeHeat: "HT-3821A",
    flangeCert: "MTR-6612",
    lubricant: "Molykote® G-1000 PTFE Thread Paste",
    targetTorque: "185",
    achievedTorque: "185",
    snugTorque: "65",
    midTorque: "130",
    finalTorque: "185",
    pattern: "Cross (Star)",
    passes: "3",
    alignmentCheck: "PASS",
    gasketCondition: "Good — no scoring or damage",
    boltEngagement: "Full thread engagement verified all 16 bolts",
    surfaceFinish: "125–250 AARH verified both flanges",
    date: "03/14/2026",
    shift: "Day",
    wrenchId: "TW-104",
    wrenchCalDue: "06/01/2026",
    inspector: "J. Reed",
    initials: "J. REED",
    result: "ACC",
    remarks: "Discharge nozzle. All bolts torqued per TQ-44A. Verified flange face parallelism prior to bolt-up."
  },
  "FLG-003": {
    id: "FLG-003",
    location: "Recycle Line Tie-In",
    size: '4"',
    cls: "600#",
    boltSize: '7/8" dia × 6.25" L',
    boltQty: "16",
    boltMat: "ASTM A193 B7",
    boltHeat: "HT-9042",
    boltCert: "MTR-8801",
    nutMat: "ASTM A194 2H",
    nutHeat: "HT-9043",
    nutCert: "MTR-8802",
    gasketType: "Spiral Wound 316SS/Flex Graphite",
    gasketStd: "ASME B16.20",
    gasketLot: "GT-2241",
    flangeMat: "ASTM A105N",
    flangeHeat: "HT-3821A",
    flangeCert: "MTR-6612",
    lubricant: "Molykote® G-1000 PTFE Thread Paste",
    targetTorque: "120",
    achievedTorque: "120",
    snugTorque: "40",
    midTorque: "80",
    finalTorque: "120",
    pattern: "Cross (Star)",
    passes: "3",
    alignmentCheck: "PASS",
    gasketCondition: "Good — no scoring or damage",
    boltEngagement: "Full thread engagement verified all 16 bolts",
    surfaceFinish: "125–250 AARH verified both flanges",
    date: "03/14/2026",
    shift: "Day",
    wrenchId: "TW-104",
    wrenchCalDue: "06/01/2026",
    inspector: "J. Reed",
    initials: "J. REED",
    result: "ACC",
    remarks: "Recycle tie-in. Verified spool alignment prior to bolt-up. No springback observed."
  },
  "FLG-004": {
    id: "FLG-004",
    location: "PSV-101 Inlet",
    size: '3"',
    cls: "600#",
    boltSize: '3/4" dia × 5.75" L',
    boltQty: "12",
    boltMat: "ASTM A193 B7",
    boltHeat: "HT-9042",
    boltCert: "MTR-8801",
    nutMat: "ASTM A194 2H",
    nutHeat: "HT-9043",
    nutCert: "MTR-8802",
    gasketType: "Spiral Wound 316SS/Flex Graphite",
    gasketStd: "ASME B16.20",
    gasketLot: "GT-2241",
    flangeMat: "ASTM A105N",
    flangeHeat: "HT-3821B",
    flangeCert: "MTR-6613",
    lubricant: "Molykote® G-1000 PTFE Thread Paste",
    targetTorque: "120",
    achievedTorque: "120",
    snugTorque: "40",
    midTorque: "80",
    finalTorque: "120",
    pattern: "Cross (Star)",
    passes: "3",
    alignmentCheck: "PASS",
    gasketCondition: "Good — no scoring or damage",
    boltEngagement: "Full thread engagement verified all 12 bolts",
    surfaceFinish: "125–250 AARH verified both flanges",
    date: "03/14/2026",
    shift: "Day",
    wrenchId: "TW-104",
    wrenchCalDue: "06/01/2026",
    inspector: "J. Reed",
    initials: "J. REED",
    result: "ACC",
    remarks: "PSV-101 inlet nozzle. Valve orientation confirmed correct prior to bolt-up. All bolts per TQ-44A."
  },
  "FLG-005": {
    id: "FLG-005",
    location: "Drain Connection",
    size: '1.5"',
    cls: "600#",
    boltSize: '5/8" dia × 4.50" L',
    boltQty: "8",
    boltMat: "ASTM A193 B7",
    boltHeat: "HT-9042",
    boltCert: "MTR-8801",
    nutMat: "ASTM A194 2H",
    nutHeat: "HT-9043",
    nutCert: "MTR-8802",
    gasketType: "Spiral Wound 316SS/Flex Graphite",
    gasketStd: "ASME B16.20",
    gasketLot: "GT-2241",
    flangeMat: "ASTM A105N",
    flangeHeat: "HT-3821B",
    flangeCert: "MTR-6613",
    lubricant: "Molykote® G-1000 PTFE Thread Paste",
    targetTorque: "65",
    achievedTorque: "65",
    snugTorque: "20",
    midTorque: "45",
    finalTorque: "65",
    pattern: "Cross (Star)",
    passes: "2",
    alignmentCheck: "PASS",
    gasketCondition: "Good — no scoring or damage",
    boltEngagement: "Full thread engagement verified all 8 bolts",
    surfaceFinish: "125–250 AARH verified both flanges",
    date: "03/14/2026",
    shift: "Day",
    wrenchId: "TW-104",
    wrenchCalDue: "06/01/2026",
    inspector: "J. Reed",
    initials: "J. REED",
    result: "ACC",
    remarks: "Drain valve connection. 2-pass per TQ-44A for 1.5\" CL600. Blind flange confirmed installed."
  }
};

// ── FORM-044A ANSWERS (Step 1) — per joint ────────────────────
var FORM_ANSWERS = {
  "FLG-001": {
    bolt_size: '1" × 7.25"',
    bolt_qty: "16",
    bolt_mat: "ASTM A193 B7",
    bolt_heat: "HT-9042",
    bolt_cert: "MTR-8801",
    nut_mat: "ASTM A194 2H",
    nut_cert: "MTR-8802",
    gasket_type: "Spiral Wound 316SS/Flex Graphite",
    gasket_std: "ASME B16.20",
    gasket_lot: "GT-2241",
    flange_mat: "ASTM A105N",
    flange_cert: "MTR-6612",
    lubricant: "Molykote G-1000",
    pattern: "Cross",
    passes: "3",
    target: "185",
    wrench_id: "TW-104",
    wrench_cal_due: "06/01/2026"
  },
  "FLG-002": {
    bolt_size: '1" × 7.25"',
    bolt_qty: "16",
    bolt_mat: "ASTM A193 B7",
    bolt_heat: "HT-9042",
    bolt_cert: "MTR-8801",
    nut_mat: "ASTM A194 2H",
    nut_cert: "MTR-8802",
    gasket_type: "Spiral Wound 316SS/Flex Graphite",
    gasket_std: "ASME B16.20",
    gasket_lot: "GT-2241",
    flange_mat: "ASTM A105N",
    flange_cert: "MTR-6612",
    lubricant: "Molykote G-1000",
    pattern: "Cross",
    passes: "3",
    target: "185",
    wrench_id: "TW-104",
    wrench_cal_due: "06/01/2026"
  },
  "FLG-003": {
    bolt_size: '7/8" × 6.25"',
    bolt_qty: "16",
    bolt_mat: "ASTM A193 B7",
    bolt_heat: "HT-9042",
    bolt_cert: "MTR-8801",
    nut_mat: "ASTM A194 2H",
    nut_cert: "MTR-8802",
    gasket_type: "Spiral Wound 316SS/Flex Graphite",
    gasket_std: "ASME B16.20",
    gasket_lot: "GT-2241",
    flange_mat: "ASTM A105N",
    flange_cert: "MTR-6612",
    lubricant: "Molykote G-1000",
    pattern: "Cross",
    passes: "3",
    target: "120",
    wrench_id: "TW-104",
    wrench_cal_due: "06/01/2026"
  },
  "FLG-004": {
    bolt_size: '3/4" × 5.75"',
    bolt_qty: "12",
    bolt_mat: "ASTM A193 B7",
    bolt_heat: "HT-9042",
    bolt_cert: "MTR-8801",
    nut_mat: "ASTM A194 2H",
    nut_cert: "MTR-8802",
    gasket_type: "Spiral Wound 316SS/Flex Graphite",
    gasket_std: "ASME B16.20",
    gasket_lot: "GT-2241",
    flange_mat: "ASTM A105N",
    flange_cert: "MTR-6613",
    lubricant: "Molykote G-1000",
    pattern: "Cross",
    passes: "3",
    target: "120",
    wrench_id: "TW-104",
    wrench_cal_due: "06/01/2026"
  },
  "FLG-005": {
    bolt_size: '5/8" × 4.50"',
    bolt_qty: "8",
    bolt_mat: "ASTM A193 B7",
    bolt_heat: "HT-9042",
    bolt_cert: "MTR-8801",
    nut_mat: "ASTM A194 2H",
    nut_cert: "MTR-8802",
    gasket_type: "Spiral Wound 316SS/Flex Graphite",
    gasket_std: "ASME B16.20",
    gasket_lot: "GT-2241",
    flange_mat: "ASTM A105N",
    flange_cert: "MTR-6613",
    lubricant: "Molykote G-1000",
    pattern: "Cross",
    passes: "2",
    target: "65",
    wrench_id: "TW-104",
    wrench_cal_due: "06/01/2026"
  }
};

// Fields that must match exactly (case-insensitive)
// Special matchers for fields that have natural variation
function checkFormField(key, userVal, correctVal) {
  var u = userVal.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
  var c = correctVal.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
  if (key === "lubricant") return u.includes("G1000") || u.includes("MOLYKOTE");
  if (key === "gasket_type") return u.includes("SPIRAL") && (u.includes("316") || u.includes("SWG"));
  if (key === "gasket_std") return u.includes("B1620");
  if (key === "flange_mat") return u.includes("A105");
  if (key === "bolt_mat") return u.includes("A193") && u.includes("B7");
  if (key === "nut_mat") return u.includes("A194") && u.includes("2H");
  return u === c;
}

// ── MTR DATA ──────────────────────────────────────────────────
var MTRS = {
  bolts: {
    title: "MILL TEST REPORT — STUD BOLTS",
    certNo: "MTR-8801",
    manufacturer: "Lone Star Fastener Co., Houston TX 77042",
    spec: "ASTM A193 / A193M",
    grade: "Grade B7",
    heatNo: "HT-9042",
    poNo: "PO-44812",
    jobNo: "MCK-2026-001",
    product: "Fully Threaded Stud Bolt, Heavy Hex",
    sizes: ['5/8" dia × 4.50" L (8 pcs)', '3/4" dia × 5.75" L (12 pcs)', '7/8" dia × 6.25" L (16 pcs)', '1" dia × 7.25" L (32 pcs)'],
    heatTreatment: "Quench & Temper per ASTM A193 §S1",
    chemistry: [["Element", "C", "Mn", "P", "S", "Si", "Cr", "Mo", "Ni"], ["Required", "0.37–0.49", "0.65–1.10", "≤0.035", "≤0.040", "0.15–0.35", "0.75–1.20", "0.15–0.25", "—"], ["Actual", "0.41", "0.82", "0.018", "0.012", "0.24", "1.04", "0.21", "0.09"]],
    mechanical: [["Property", "Requirement", "Actual"], ["Tensile Strength", "≥125 ksi (862 MPa)", "138 ksi"], ["Yield Strength (0.2%)", "≥105 ksi (724 MPa)", "119 ksi"], ["Elongation in 2\"", "≥16%", "21%"], ["Reduction of Area", "≥50%", "63%"], ["Hardness", "≤35 HRC", "28 HRC"]],
    certification: "We hereby certify that the material described herein has been manufactured, sampled, tested, and inspected in accordance with ASTM A193/A193M Grade B7 and that the results meet all the requirements of said specification.",
    certifiedBy: "R. Whitfield, QA Manager",
    certDate: "2025-10-14",
    sourNote: "Hardness confirmed ≤35 HRC per NACE MR0175 / ISO 15156 requirements for sour service."
  },
  nuts: {
    title: "MILL TEST REPORT — HEAVY HEX NUTS",
    certNo: "MTR-8802",
    manufacturer: "Lone Star Fastener Co., Houston TX 77042",
    spec: "ASTM A194 / A194M",
    grade: "Grade 2H",
    heatNo: "HT-9043",
    poNo: "PO-44812",
    jobNo: "MCK-2026-001",
    product: "Heavy Hex Nut, per ASME B18.2.2",
    sizes: ['5/8"–11 UNC', '3/4"–10 UNC', '7/8"–9 UNC', '1"–8 UNC'],
    heatTreatment: "Quench & Temper",
    chemistry: [["Element", "C", "Mn", "P", "S"], ["Required", "0.40–0.53", "0.57–0.90", "≤0.040", "≤0.050"], ["Actual", "0.46", "0.74", "0.021", "0.018"]],
    mechanical: [["Property", "Requirement", "Actual"], ["Proof Load Stress", "175 ksi", "182 ksi"], ["Hardness", "C24–C36", "C29"]],
    certification: "We hereby certify that the material described herein conforms to ASTM A194/A194M Grade 2H. All chemical and mechanical test results meet specification requirements.",
    certifiedBy: "R. Whitfield, QA Manager",
    certDate: "2025-10-14",
    sourNote: null
  },
  flangesA: {
    title: "MILL TEST REPORT — WELD NECK FLANGES (Heat A)",
    certNo: "MTR-6612",
    manufacturer: "Gulf Coast Forgings LLC, Beaumont TX 77703",
    spec: "ASTM A105 / A105M",
    grade: "Normalized (A105N)",
    heatNo: "HT-3821A",
    poNo: "PO-44789",
    jobNo: "MCK-2026-001",
    product: 'Weld Neck Flange RF, ASME B16.5 Class 600',
    sizes: ['4" 600# WN RF (1 pc)', '6" 600# WN RF (2 pcs)'],
    heatTreatment: "Normalized at 1650°F, Air Cooled",
    chemistry: [["Element", "C", "Mn", "P", "S", "Si", "Cu", "Ni", "Cr", "Mo", "V"], ["Required", "≤0.35", "0.60–1.05", "≤0.035", "≤0.040", "0.10–0.35", "≤0.40", "≤0.40", "≤0.30", "≤0.12", "≤0.08"], ["Actual", "0.28", "0.88", "0.014", "0.009", "0.22", "0.06", "0.07", "0.08", "0.04", "0.02"]],
    mechanical: [["Property", "Requirement", "Actual"], ["Tensile Strength", "≥70 ksi (485 MPa)", "78 ksi"], ["Yield Strength (0.2%)", "≥36 ksi (250 MPa)", "52 ksi"], ["Elongation in 2\"", "≥22%", "29%"], ["Reduction of Area", "≥30%", "48%"], ["Charpy Impact (−20°F)", "15 ft-lb avg", "22 ft-lb avg"]],
    certification: "We hereby certify that all material described herein was manufactured, heat treated, tested, and inspected in accordance with ASTM A105/A105M. All results conform to specification requirements.",
    certifiedBy: "D. Tanner, Metallurgical QA",
    certDate: "2025-09-22",
    sourNote: null
  },
  flangesB: {
    title: "MILL TEST REPORT — WELD NECK FLANGES (Heat B)",
    certNo: "MTR-6613",
    manufacturer: "Gulf Coast Forgings LLC, Beaumont TX 77703",
    spec: "ASTM A105 / A105M",
    grade: "Normalized (A105N)",
    heatNo: "HT-3821B",
    poNo: "PO-44789",
    jobNo: "MCK-2026-001",
    product: 'Weld Neck Flange RF, ASME B16.5 Class 600',
    sizes: ['1.5" 600# WN RF (1 pc)', '3" 600# WN RF (1 pc)'],
    heatTreatment: "Normalized at 1650°F, Air Cooled",
    chemistry: [["Element", "C", "Mn", "P", "S", "Si", "Cu", "Ni", "Cr", "Mo", "V"], ["Required", "≤0.35", "0.60–1.05", "≤0.035", "≤0.040", "0.10–0.35", "≤0.40", "≤0.40", "≤0.30", "≤0.12", "≤0.08"], ["Actual", "0.26", "0.91", "0.016", "0.011", "0.19", "0.08", "0.05", "0.07", "0.03", "0.01"]],
    mechanical: [["Property", "Requirement", "Actual"], ["Tensile Strength", "≥70 ksi (485 MPa)", "74 ksi"], ["Yield Strength (0.2%)", "≥36 ksi (250 MPa)", "49 ksi"], ["Elongation in 2\"", "≥22%", "31%"], ["Reduction of Area", "≥30%", "51%"], ["Charpy Impact (−20°F)", "15 ft-lb avg", "19 ft-lb avg"]],
    certification: "We hereby certify that all material described herein was manufactured, heat treated, tested, and inspected in accordance with ASTM A105/A105M. All results conform to specification requirements.",
    certifiedBy: "D. Tanner, Metallurgical QA",
    certDate: "2025-09-22",
    sourNote: null
  },
  gaskets: {
    title: "CERTIFICATE OF CONFORMANCE — SPIRAL WOUND GASKETS",
    certNo: "GT-2241",
    manufacturer: "Flexseal Gasket Industries, Inc., Deer Park TX 77536",
    spec: "ASME B16.20",
    grade: "Spiral Wound — 316SS / Flexible Graphite",
    heatNo: "N/A",
    lotNo: "GT-2241",
    poNo: "PO-44801",
    jobNo: "MCK-2026-001",
    product: "Spiral Wound Gasket with Centering Ring & Inner Retaining Ring",
    sizes: ['1.5" 600# RF SWG (4 pcs)', '3" 600# RF SWG (6 pcs)', '4" 600# RF SWG (6 pcs)', '6" 600# RF SWG (6 pcs)'],
    heatTreatment: "N/A",
    chemistry: [["Component", "Specification", "Material"], ["Winding Strip", "316 Stainless Steel", "UNS S31600"], ["Filler", "Flexible Graphite", "ASTM C782 Grade"], ["Outer Centering Ring", "Carbon Steel", "ASTM A36"], ["Inner Retaining Ring", "Carbon Steel", "ASTM A36"]],
    mechanical: [["Property", "Value"], ["Max. Operating Temp.", "500°F (260°C)"], ["Max. Operating Pressure", "2220 psi (Class 600 rating at 100°F)"], ["Seating Stress", "10,000 psi min."], ["Density (filler)", "≥1.0 g/cm³"]],
    certification: "Flexseal Gasket Industries certifies that the gaskets in Lot GT-2241 were manufactured and tested in accordance with ASME B16.20. Winding material, filler material, and ring dimensions comply with specification. These gaskets are suitable for sour gas and natural gas service per NACE MR0175.",
    certifiedBy: "M. Santos, Quality Director",
    certDate: "2025-11-03",
    sourNote: "Confirmed suitable for sour service (H₂S) per NACE MR0175 / ISO 15156."
  }
};
var CAL_CERT = {
  instrumentId: "TW-104",
  description: "Click-Type Torque Wrench, 3/4\" Drive",
  manufacturer: "Snap-on Industrial",
  model: "TECH3FR250",
  serialNo: "SN-TW-104-2019",
  range: "50 – 500 ft-lb",
  resolution: "1 ft-lb",
  accuracy: "±3% of reading (clockwise)",
  calProcedure: "MEP-QC-PROC-012 Rev. 4 / ASME B107.300",
  calStandard: "NIST-Traceable Torque Standard, Cal Lab Ref. STD-TQ-009",
  calDate: "12/01/2025",
  calDue: "06/01/2026",
  calBy: "Precision Cal Services LLC, Pasadena TX 77504",
  calTech: "A. Nguyen, Lead Calibration Technician",
  certNo: "PCAL-2025-10482",
  results: [["25% (125 ft-lb)", "125 ft-lb", "123.8 ft-lb", "-0.96%", "PASS"], ["50% (250 ft-lb)", "250 ft-lb", "248.1 ft-lb", "-0.76%", "PASS"], ["75% (375 ft-lb)", "375 ft-lb", "373.2 ft-lb", "-0.48%", "PASS"], ["100% (500 ft-lb)", "500 ft-lb", "497.6 ft-lb", "-0.48%", "PASS"]],
  status: "CALIBRATED — IN TOLERANCE",
  nextCalNote: "Return for calibration by 06/01/2026. Do not use after this date without recalibration. Tag wrench with calibration label #PCL-104."
};
var amber = "#d4832a",
  green = "#52a366",
  red = "#c95f5f",
  steel = "#3a556a",
  bg = "#0e0f0d",
  surf = "#161714",
  surf2 = "#1d1f1b",
  border = "#2a2d27",
  textCol = "#ccc8be",
  muted = "#6e6b63",
  white = "#ede8df";
var mono = "'IBM Plex Mono', monospace";

// ── MTR PANEL ─────────────────────────────────────────────────
function MTRPanel() {
  var _useState = useState("bolts"),
    _useState2 = _slicedToArray(_useState, 2),
    active = _useState2[0],
    setActive = _useState2[1]; // MTR component
  var tabs = [["bolts", "Bolts (A193 B7)"], ["nuts", "Nuts (A194 2H)"], ["flangesA", "Flanges Heat A"], ["flangesB", "Flanges Heat B"], ["gaskets", "Gasket Cert"]];
  var m = MTRS[active];
  var MtrTable = function MtrTable(_ref) {
    var data = _ref.data;
    return /*#__PURE__*/React.createElement("table", {
      style: {
        borderCollapse: "collapse",
        width: "100%",
        fontSize: "8.5px",
        marginTop: "4px",
        marginBottom: "8px"
      }
    }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
      style: {
        background: "#111410"
      }
    }, data[0].map(function (h, i) {
      return /*#__PURE__*/React.createElement("th", {
        key: i,
        style: {
          padding: "4px 7px",
          textAlign: "left",
          color: amber,
          fontSize: "7.5px",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          borderBottom: "1px solid ".concat(border),
          borderRight: i < data[0].length - 1 ? "1px solid ".concat(border) : "none",
          fontWeight: 700
        }
      }, h);
    }))), /*#__PURE__*/React.createElement("tbody", null, data.slice(1).map(function (row, ri) {
      return /*#__PURE__*/React.createElement("tr", {
        key: ri,
        style: {
          background: ri % 2 === 0 ? "transparent" : "rgba(255,255,255,0.02)"
        }
      }, row.map(function (cell, ci) {
        return /*#__PURE__*/React.createElement("td", {
          key: ci,
          style: {
            padding: "4px 7px",
            color: ci === 0 ? muted : ri === data.length - 2 && ci > 0 ? "#8ec89a" : textCol,
            fontSize: "8.5px",
            borderBottom: "1px solid #1a1c18",
            borderRight: ci < row.length - 1 ? "1px solid ".concat(border) : "none",
            fontWeight: ci === 0 ? "600" : "400"
          }
        }, cell);
      }));
    })));
  };
  var Field = function Field(_ref2) {
    var label = _ref2.label,
      value = _ref2.value,
      _ref2$hi = _ref2.hi,
      hi = _ref2$hi === void 0 ? false : _ref2$hi,
      _ref2$green = _ref2.green,
      green = _ref2$green === void 0 ? false : _ref2$green;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: "grid",
        gridTemplateColumns: "130px 1fr",
        borderBottom: "1px solid #1a1c18",
        minHeight: "22px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "4px 8px",
        background: surf2,
        color: textCol,
        fontSize: "7.5px",
        letterSpacing: "0.07em",
        textTransform: "uppercase",
        borderRight: "1px solid ".concat(border),
        display: "flex",
        alignItems: "center"
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "4px 8px",
        color: green ? "#52a366" : hi ? white : textCol,
        fontSize: hi ? "9.5px" : "8.5px",
        fontWeight: hi ? "700" : "400",
        display: "flex",
        alignItems: "center"
      }
    }, value));
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "0"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      borderBottom: "1px solid ".concat(border),
      marginBottom: "10px"
    }
  }, tabs.map(function (_ref3) {
    var _ref4 = _slicedToArray(_ref3, 2),
      id = _ref4[0],
      label = _ref4[1];
    return /*#__PURE__*/React.createElement("button", {
      key: id,
      onClick: function onClick() {
        return setActive(id);
      },
      style: {
        background: active === id ? "rgba(212,131,42,0.1)" : "none",
        border: "none",
        borderBottom: active === id ? "2px solid ".concat(amber) : "2px solid transparent",
        color: active === id ? amber : muted,
        cursor: "pointer",
        padding: "6px 10px",
        fontFamily: mono,
        fontSize: "7.5px",
        letterSpacing: "0.1em",
        textTransform: "uppercase"
      }
    }, label);
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid ".concat(border),
      background: surf
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(212,131,42,0.08)",
      borderBottom: "1px solid ".concat(border),
      padding: "8px 10px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "9px",
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase"
    }
  }, m.title), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      marginTop: "2px"
    }
  }, m.manufacturer)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      borderBottom: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRight: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement(Field, {
    label: "Cert / Lot No.",
    value: active === "gaskets" ? m.lotNo : m.certNo,
    hi: true,
    green: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Specification",
    value: m.spec,
    hi: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Grade",
    value: m.grade,
    hi: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: active === "gaskets" ? "Lot No." : "Heat No.",
    value: active === "gaskets" ? m.lotNo : m.heatNo,
    hi: true
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Field, {
    label: "PO No.",
    value: m.poNo
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Job No.",
    value: m.jobNo
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Product",
    value: m.product
  }), /*#__PURE__*/React.createElement(Field, {
    label: active === "gaskets" ? "" : "Heat Treatment",
    value: active === "gaskets" ? "" : m.heatTreatment
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "8px 10px"
    }
  }, active !== "gaskets" && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "4px"
    }
  }, "Sizes / Quantities Covered"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: "4px",
      marginBottom: "10px"
    }
  }, m.sizes.map(function (s) {
    return /*#__PURE__*/React.createElement("span", {
      key: s,
      style: {
        background: "#111410",
        border: "1px solid ".concat(border),
        color: textCol,
        fontSize: "8px",
        padding: "2px 8px"
      }
    }, s);
  }))), active === "gaskets" && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "4px"
    }
  }, "Sizes / Quantities Covered"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: "4px",
      marginBottom: "10px"
    }
  }, m.sizes.map(function (s) {
    return /*#__PURE__*/React.createElement("span", {
      key: s,
      style: {
        background: "#111410",
        border: "1px solid ".concat(border),
        color: textCol,
        fontSize: "8px",
        padding: "2px 8px"
      }
    }, s);
  }))), active === "gaskets" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "2px"
    }
  }, "Materials"), /*#__PURE__*/React.createElement(MtrTable, {
    data: m.chemistry
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "2px"
    }
  }, "Performance Properties"), /*#__PURE__*/React.createElement(MtrTable, {
    data: m.mechanical
  })) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "2px"
    }
  }, "Chemical Analysis (%)"), /*#__PURE__*/React.createElement(MtrTable, {
    data: m.chemistry
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "2px"
    }
  }, "Mechanical Properties"), /*#__PURE__*/React.createElement(MtrTable, {
    data: m.mechanical
  })), m.sourNote && /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(82,163,102,0.08)",
      border: "1px solid rgba(82,163,102,0.25)",
      padding: "6px 8px",
      marginBottom: "8px",
      fontSize: "8.5px",
      color: "#a0d4a8"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "#52a366",
      fontWeight: 700,
      marginRight: "6px"
    }
  }, "\u2713 SOUR SERVICE"), m.sourNote), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#0d100b",
      border: "1px solid ".concat(border),
      padding: "8px 10px",
      marginBottom: "6px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      marginBottom: "3px"
    }
  }, "Certification Statement"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: textCol,
      fontSize: "8.5px",
      lineHeight: 1.6,
      fontStyle: "italic"
    }
  }, m.certification)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "0"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "4px 0"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.08em",
      textTransform: "uppercase"
    }
  }, "Certified By: "), /*#__PURE__*/React.createElement("span", {
    style: {
      color: white,
      fontSize: "8.5px"
    }
  }, m.certifiedBy)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "4px 0",
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.08em",
      textTransform: "uppercase"
    }
  }, "Cert Date: "), /*#__PURE__*/React.createElement("span", {
    style: {
      color: white,
      fontSize: "8.5px"
    }
  }, m.certDate))))));
}

// ── CALIBRATION CERT ──────────────────────────────────────────
function CalCertPanel() {
  var c = CAL_CERT;
  var Field = function Field(_ref5) {
    var label = _ref5.label,
      value = _ref5.value,
      _ref5$hi = _ref5.hi,
      hi = _ref5$hi === void 0 ? false : _ref5$hi,
      _ref5$accent = _ref5.accent,
      accent = _ref5$accent === void 0 ? false : _ref5$accent,
      _ref5$warn = _ref5.warn,
      warn = _ref5$warn === void 0 ? false : _ref5$warn;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: "grid",
        gridTemplateColumns: "160px 1fr",
        borderBottom: "1px solid #1a1c18",
        minHeight: "22px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "4px 8px",
        background: surf2,
        color: textCol,
        fontSize: "7.5px",
        letterSpacing: "0.07em",
        textTransform: "uppercase",
        borderRight: "1px solid ".concat(border),
        display: "flex",
        alignItems: "center"
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "4px 8px",
        color: warn ? "#c95f5f" : accent ? amber : hi ? white : textCol,
        fontSize: hi ? "9.5px" : "8.5px",
        fontWeight: hi ? "700" : "400",
        display: "flex",
        alignItems: "center"
      }
    }, value));
  };
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid ".concat(border),
      background: surf
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(212,131,42,0.08)",
      borderBottom: "2px solid ".concat(amber),
      padding: "8px 10px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "9px",
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase"
    }
  }, "CALIBRATION CERTIFICATE"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      marginTop: "2px"
    }
  }, "Precision Cal Services LLC, Pasadena TX 77504")), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(82,163,102,0.15)",
      border: "1px solid rgba(82,163,102,0.4)",
      padding: "4px 10px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: "#52a366",
      fontSize: "8px",
      fontWeight: 700,
      letterSpacing: "0.1em"
    }
  }, c.status))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      borderBottom: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRight: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement(Field, {
    label: "Instrument ID",
    value: c.instrumentId,
    hi: true,
    accent: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Description",
    value: c.description,
    hi: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Manufacturer",
    value: c.manufacturer
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Model No.",
    value: c.model
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Serial No.",
    value: c.serialNo
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Field, {
    label: "Cert No.",
    value: c.certNo
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Calibration Date",
    value: c.calDate
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Calibration Due",
    value: c.calDue,
    hi: true,
    accent: true
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Range",
    value: c.range
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Accuracy",
    value: c.accuracy
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      borderBottom: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement(Field, {
    label: "Cal Procedure",
    value: c.calProcedure
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Reference Standard",
    value: c.calStandard
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Calibrated By",
    value: c.calBy
  }), /*#__PURE__*/React.createElement(Field, {
    label: "Cal Technician",
    value: c.calTech
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "10px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "6px"
    }
  }, "Calibration Results \u2014 As Found / As Left"), /*#__PURE__*/React.createElement("table", {
    style: {
      borderCollapse: "collapse",
      width: "100%",
      fontSize: "8.5px",
      marginBottom: "10px"
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: "#111410"
    }
  }, ["Test Point", "Applied (Reference)", "Indicated (Wrench)", "Error", "Result"].map(function (h, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      style: {
        padding: "4px 8px",
        textAlign: "left",
        color: amber,
        fontSize: "7px",
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        borderBottom: "1px solid ".concat(border),
        borderRight: i < 4 ? "1px solid ".concat(border) : "none",
        fontWeight: 700
      }
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, c.results.map(function (row, i) {
    return /*#__PURE__*/React.createElement("tr", {
      key: i,
      style: {
        background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.02)"
      }
    }, row.map(function (cell, ci) {
      return /*#__PURE__*/React.createElement("td", {
        key: ci,
        style: {
          padding: "4px 8px",
          color: ci === 4 ? "#52a366" : ci === 3 ? textCol : ci === 0 ? muted : textCol,
          fontSize: "8.5px",
          fontWeight: ci === 4 ? "700" : "400",
          borderBottom: "1px solid #1a1c18",
          borderRight: ci < 4 ? "1px solid ".concat(border) : "none"
        }
      }, cell);
    }));
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(212,131,42,0.06)",
      border: "1px solid rgba(212,131,42,0.2)",
      borderLeft: "3px solid ".concat(amber),
      padding: "7px 10px",
      fontSize: "8.5px",
      color: textCol,
      lineHeight: 1.6
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: amber,
      fontWeight: 700,
      marginRight: "6px"
    }
  }, "NOTE:"), c.nextCalNote))));
}

// ── STEP 1: MEP-QC-FORM-044A (Pre-Assembly) ───────────────────
function PreAssemblyForm(_ref6) {
  var onComplete = _ref6.onComplete;
  var _useState3 = useState("FLG-001"),
    _useState4 = _slicedToArray(_useState3, 2),
    activeJoint = _useState4[0],
    setActiveJoint = _useState4[1];
  var _useState5 = useState(function () {
      return Object.fromEntries(SCENARIO.joints.map(function (j) {
        return [j.id, {
          bolt_size: "",
          bolt_qty: "",
          bolt_mat: "",
          bolt_heat: "",
          bolt_cert: "",
          nut_mat: "",
          nut_cert: "",
          gasket_type: "",
          gasket_std: "",
          gasket_lot: "",
          flange_mat: "",
          flange_cert: "",
          lubricant: "",
          pattern: "",
          passes: "",
          target: "",
          wrench_id: "",
          wrench_cal_due: ""
        }];
      }));
    }),
    _useState6 = _slicedToArray(_useState5, 2),
    formData = _useState6[0],
    setFormData = _useState6[1];
  var _useState7 = useState(false),
    _useState8 = _slicedToArray(_useState7, 2),
    submitted = _useState8[0],
    setSubmitted = _useState8[1];
  var _useState9 = useState(null),
    _useState0 = _slicedToArray(_useState9, 2),
    scores = _useState0[0],
    setScores = _useState0[1];
  var _useState1 = useState(null),
    _useState10 = _slicedToArray(_useState1, 2),
    totalScore = _useState10[0],
    setTotalScore = _useState10[1];
  var inputRefs = useRef({});
  var joint = SCENARIO.joints.find(function (j) {
    return j.id === activeJoint;
  });
  var SCORED_FIELDS = [{
    key: "bolt_size",
    label: "Bolt Size / Length",
    hint: 'Format: diameter × length — match exactly as listed on the MTR (e.g. ½" × 3.25")',
    tooltip: "Find bolt size for this NPS and class on the MTR. Record diameter × length.",
    section: "bolting"
  }, {
    key: "bolt_qty",
    label: "Bolt Quantity",
    hint: "Whole number — count from BOM or MTR for this flange size and class",
    tooltip: "Numeric count only. Find the quantity for this specific NPS and class.",
    section: "bolting"
  }, {
    key: "bolt_mat",
    label: "Bolt Material / Spec",
    hint: "Format: ASTM AXXXX Grade XX — match the Specification and Grade fields on the MTR exactly",
    tooltip: "Copy the Specification and Grade from the bolt MTR verbatim.",
    section: "bolting"
  }, {
    key: "bolt_heat",
    label: "Bolt Heat No.",
    hint: "Format: HT-XXXX — copy exactly as printed in the Heat No. field on the MTR",
    tooltip: "Located in the header block of the bolt MTR. Do not guess or abbreviate.",
    section: "bolting"
  }, {
    key: "bolt_cert",
    label: "Bolt Cert No. (MTR)",
    hint: "Format: MTR-XXXX — copy the Cert No. from the top of the bolt MTR exactly",
    tooltip: "This is the document number at the top of the Mill Test Report, not the heat number.",
    section: "bolting"
  }, {
    key: "nut_mat",
    label: "Nut Material / Spec",
    hint: "Format: ASTM AXXXX Grade XX — match Specification and Grade on the nut MTR exactly",
    tooltip: "Copy from the nut MTR, not the bolt MTR — they are separate documents.",
    section: "bolting"
  }, {
    key: "nut_cert",
    label: "Nut Cert No. (MTR)",
    hint: "Format: MTR-XXXX — copy the Cert No. from the nut MTR exactly",
    tooltip: "Nut MTR is a separate cert from the bolt MTR. Both are required.",
    section: "bolting"
  }, {
    key: "gasket_type",
    label: "Gasket Type",
    hint: "Describe winding material and filler — match the gasket cert Product/Materials fields",
    tooltip: "Include both the winding strip material and the filler material as stated on the cert.",
    section: "gasket"
  }, {
    key: "gasket_std",
    label: "Gasket Standard",
    hint: "Format: ASME BXX.XX — the manufacturing standard the gasket is certified to",
    tooltip: "Found on the gasket cert. This is the standard that governs the gasket construction.",
    section: "gasket"
  }, {
    key: "gasket_lot",
    label: "Gasket Lot No.",
    hint: "Format: XX-XXXX — copy the Lot No. exactly from the gasket certificate",
    tooltip: "This is the traceability number for this batch of gaskets. Exact match required.",
    section: "gasket"
  }, {
    key: "flange_mat",
    label: "Flange Material / Spec",
    hint: "Format: ASTM AXXXX + designation (e.g. normalized suffix) — from the flange MTR Grade field",
    tooltip: "Use the Spec field AND Grade field from the flange MTR. There are two flange heats — verify which covers this joint's size.",
    section: "flange"
  }, {
    key: "flange_cert",
    label: "Flange Cert No. (MTR)",
    hint: "Format: MTR-XXXX — copy exactly from the flange MTR cert header. Note: cert may differ by flange size.",
    tooltip: "There are two flange MTRs (Heat A and Heat B). Check which sizes each covers before selecting.",
    section: "flange"
  }, {
    key: "lubricant",
    label: "Lubricant",
    hint: "Brand name and product designation — specified in the company spec §7.1",
    tooltip: "The approved lubricant is named in the specification. Record the brand and product name.",
    section: "install"
  }, {
    key: "pattern",
    label: "Tightening Pattern",
    hint: "Single word or short phrase — the tightening sequence method required by the spec §8.3",
    tooltip: "Named explicitly in the spec. This is the bolt tightening sequence method, not a torque value.",
    section: "install"
  }, {
    key: "passes",
    label: "Number of Passes",
    hint: "Whole number — find in spec Table 1 for this NPS. Note: smaller sizes may differ from larger.",
    tooltip: "Look up this specific NPS in Table 1. The pass count is in the Min. Passes column.",
    section: "install"
  }, {
    key: "target",
    label: "Target Torque (ft-lb)",
    hint: "Whole number, ft-lb — look up this NPS and class in spec Table 1, Final Torque column",
    tooltip: "Use the Final Torque column in Table 1. Match NPS exactly — do not interpolate.",
    section: "install"
  }, {
    key: "wrench_id",
    label: "Torque Wrench ID",
    hint: "Format: TW-XXX — copy the Instrument ID exactly from the calibration certificate",
    tooltip: "Found in the header of the calibration certificate. This ID links the work record to the instrument.",
    section: "equip"
  }, {
    key: "wrench_cal_due",
    label: "Wrench Cal. Due Date",
    hint: "Format: MM/DD/YYYY — copy the Calibration Due date from the cal cert exactly",
    tooltip: "If this date has passed, the wrench cannot be used. Find it in the cal cert header.",
    section: "equip"
  }];
  var SECTIONS = [{
    id: "bolting",
    label: "Bolt & Nut Material Traceability",
    color: amber
  }, {
    id: "gasket",
    label: "Gasket Material Traceability",
    color: "#8ab4c4"
  }, {
    id: "flange",
    label: "Flange Material Traceability",
    color: "#a0c8a0"
  }, {
    id: "install",
    label: "Installation Parameters",
    color: amber
  }, {
    id: "equip",
    label: "Inspection Equipment",
    color: "#c4a882"
  }];
  var update = function update(jid, key, val) {
    return setFormData(function (p) {
      return _objectSpread(_objectSpread({}, p), {}, _defineProperty({}, jid, _objectSpread(_objectSpread({}, p[jid]), {}, _defineProperty({}, key, val))));
    });
  };
  var allFilled = SCORED_FIELDS.every(function (f) {
    return formData["FLG-001"][f.key].trim() !== "";
  });
  var handleSubmit = function handleSubmit() {
    var totalCor = 0,
      totalFields = 0;
    var sc = {};
    var j = "FLG-001";
    sc[j] = {};
    SCORED_FIELDS.forEach(function (f) {
      totalFields++;
      var ok = checkFormField(f.key, formData[j][f.key], FORM_ANSWERS[j][f.key]);
      if (ok) totalCor++;
      sc[j][f.key] = {
        ok: ok,
        entered: formData[j][f.key],
        correct: FORM_ANSWERS[j][f.key]
      };
    });
    setScores(sc);
    setTotalScore(Math.round(totalCor / totalFields * 100));
    setSubmitted(true);
  };
  var reset = function reset() {
    setFormData(Object.fromEntries(SCENARIO.joints.map(function (j) {
      return [j.id, Object.fromEntries(SCORED_FIELDS.map(function (f) {
        return [f.key, ""];
      }))];
    })));
    setSubmitted(false);
    setScores(null);
    setTotalScore(null);
  };
  var passed = totalScore !== null && totalScore >= 80;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: mono
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(212,131,42,0.08)",
      border: "1px solid ".concat(border),
      borderTop: "2px solid ".concat(amber),
      padding: "8px 12px",
      marginBottom: "12px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "8px",
      letterSpacing: "0.18em",
      textTransform: "uppercase",
      marginBottom: "3px"
    }
  }, "Mustang Energy Partners, LLC"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: white,
      fontSize: "12px",
      fontWeight: 700,
      letterSpacing: "0.04em"
    }
  }, "FLANGE CONNECTION TORQUE RECORD"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "8px",
      marginTop: "2px"
    }
  }, "MEP-QC-FORM-044A Rev. 3 \xB7 Pre-Assembly Section")), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      textTransform: "uppercase",
      letterSpacing: "0.1em"
    }
  }, "Form No."), /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "11px",
      fontWeight: 700
    }
  }, "MEP-QC-FORM-044A"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      marginTop: "2px"
    }
  }, SCENARIO.project), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px"
    }
  }, SCENARIO.system))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "8px",
      padding: "6px 8px",
      background: "rgba(0,0,0,0.3)",
      border: "1px solid ".concat(border),
      fontSize: "8.5px",
      color: "#8ab4c4",
      fontStyle: "italic"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "#8ab4c4",
      fontWeight: 700,
      marginRight: "6px"
    }
  }, "INSTRUCTIONS:"), "Complete all fields below using the ISO Drawing, Bill of Materials, Mill Test Reports, Calibration Certificate, and Company Specification (MEP-PIP-SPEC-044). Do NOT fill in Achieved Torque, Date, or Result \u2014 those are recorded after physical assembly is complete.")), submitted && /*#__PURE__*/React.createElement("div", {
    style: {
      background: passed ? "rgba(82,163,102,0.1)" : "rgba(201,95,95,0.08)",
      border: "1px solid ".concat(passed ? "rgba(82,163,102,0.3)" : "rgba(201,95,95,0.3)"),
      padding: "9px 12px",
      marginBottom: "12px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: passed ? green : red,
      fontWeight: 700,
      fontSize: "12px"
    }
  }, "Step 1 ", passed ? "✓ PASSED" : "✗ NOT PASSED", " \u2014 ", totalScore, "% on FLG-001", /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "9px",
      fontWeight: 400,
      marginLeft: "8px"
    }
  }, "Min. 80% required. Incorrect fields shown in red with correct answers in green.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "8px"
    }
  }, !passed && /*#__PURE__*/React.createElement("button", {
    onClick: reset,
    style: {
      background: "none",
      border: "1px solid ".concat(border),
      color: muted,
      padding: "5px 10px",
      cursor: "pointer",
      fontFamily: mono,
      fontSize: "8px",
      letterSpacing: "0.1em",
      textTransform: "uppercase"
    }
  }, "Retry"), passed && /*#__PURE__*/React.createElement("button", {
    onClick: function onClick() {
      return onComplete();
    },
    style: {
      background: amber,
      color: bg,
      border: "none",
      padding: "7px 14px",
      cursor: "pointer",
      fontFamily: mono,
      fontSize: "9px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      fontWeight: 700
    }
  }, "Proceed to Torque Log \u2192"))), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid ".concat(border),
      marginBottom: "8px",
      background: surf
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "5px 10px",
      background: "rgba(255,255,255,0.03)",
      borderBottom: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, "Joint Identification ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      marginLeft: "8px"
    }
  }, "(from Isometric Drawing \u2014 pre-populated)"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr"
    }
  }, [["Joint ID", joint.id], ["Location", joint.location], ["Line Size", joint.size], ["Pressure Class", "600#"], ["Fluid Service", SCENARIO.service]].map(function (_ref8, i) {
    var _ref9 = _slicedToArray(_ref8, 2),
      l = _ref9[0],
      v = _ref9[1];
    return /*#__PURE__*/React.createElement("div", {
      key: l,
      style: {
        padding: "6px 10px",
        borderRight: i < 4 ? "1px solid ".concat(border) : "none"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: muted,
        fontSize: "7px",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        marginBottom: "2px"
      }
    }, l), /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#4a6a52",
        fontSize: "10px",
        fontWeight: 600
      }
    }, v));
  }))), SECTIONS.map(function (sec) {
    var fields = SCORED_FIELDS.filter(function (f) {
      return f.section === sec.id;
    });
    return /*#__PURE__*/React.createElement("div", {
      key: sec.id,
      style: {
        border: "1px solid ".concat(border),
        marginBottom: "8px",
        background: surf
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "5px 10px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid ".concat(border),
        borderLeft: "2px solid ".concat(sec.color)
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: sec.color,
        fontSize: "7.5px",
        letterSpacing: "0.14em",
        textTransform: "uppercase"
      }
    }, sec.label), sec.id === "bolting" && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#7a9db0",
        fontSize: "7px",
        marginLeft: "10px"
      }
    }, "\u2192 See Mill Test Reports (MTR tab)"), sec.id === "gasket" && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#7a9db0",
        fontSize: "7px",
        marginLeft: "10px"
      }
    }, "\u2192 See MTR tab (Gasket Cert) and Bill of Materials on ISO Drawing"), sec.id === "flange" && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#7a9db0",
        fontSize: "7px",
        marginLeft: "10px"
      }
    }, "\u2192 See Mill Test Reports \u2014 Flanges Heat A or B (note: cert varies by joint)"), sec.id === "install" && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#7a9db0",
        fontSize: "7px",
        marginLeft: "10px"
      }
    }, "\u2192 See Company Spec (MEP-PIP-SPEC-044) \xA77.1, \xA78.1\u20138.4, Table 1"), sec.id === "equip" && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#7a9db0",
        fontSize: "7px",
        marginLeft: "10px"
      }
    }, "\u2192 See Calibration Certificate (Cal Cert tab)")), /*#__PURE__*/React.createElement("div", null, fields.map(function (field, fi) {
      return /*#__PURE__*/React.createElement("div", {
        key: field.key,
        style: {
          display: "grid",
          gridTemplateColumns: "200px 1fr",
          borderBottom: fi < fields.length - 1 ? "1px solid #1a1c18" : "none"
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          padding: "6px 10px",
          background: surf2,
          borderRight: "1px solid ".concat(border)
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          display: "flex",
          alignItems: "center"
        }
      }, /*#__PURE__*/React.createElement("span", {
        style: {
          color: textCol,
          fontSize: "7.5px",
          letterSpacing: "0.07em",
          textTransform: "uppercase",
          fontWeight: 600
        }
      }, field.label), field.tooltip && !submitted && /*#__PURE__*/React.createElement("span", {
        className: "tip-wrap"
      }, /*#__PURE__*/React.createElement("span", {
        className: "tip-icon"
      }, "i"), /*#__PURE__*/React.createElement("span", {
        className: "tip-box"
      }, field.tooltip))), /*#__PURE__*/React.createElement("div", {
        style: {
          color: "#8a9ea8",
          fontSize: "7px",
          lineHeight: 1.5,
          fontStyle: "italic",
          marginTop: "3px"
        }
      }, field.hint)), /*#__PURE__*/React.createElement("div", null, (function () {
        var jidKey = "FLG-001";
        var ck = jidKey + "|" + field.key;
        var fr = submitted && scores && scores[jidKey] && scores[jidKey][field.key];
        var wrapStyle = submitted
          ? { outline: "1.5px solid " + (fr && fr.ok ? "rgba(82,163,102,0.4)" : "rgba(201,95,95,0.35)"), background: fr && fr.ok ? "rgba(82,163,102,0.08)" : "rgba(201,95,95,0.08)" }
          : { outline: "1px solid #2a4a2a", background: "rgba(42,74,42,0.08)", transition: "outline 0.15s" };
        return React.createElement("div", { className: "fdq-form-input-wrap", style: wrapStyle },
          React.createElement("input", {
            className: "fdq-form-input",
            ref: function (el) { if (el) inputRefs.current[ck] = el; },
            value: formData["FLG-001"][field.key],
            disabled: submitted,
            onChange: function (e) { update("FLG-001", field.key, e.target.value); },
            placeholder: field.hint,
            style: {
              width: "100%",
              background: "transparent",
              border: "none",
              outline: "none",
              color: submitted ? (fr && fr.ok ? "#52a366" : "#c95f5f") : "#ede8df",
              padding: "5px 8px",
              fontSize: "10px",
              fontFamily: "'IBM Plex Mono', monospace",
              cursor: submitted ? "default" : "text",
              boxSizing: "border-box"
            }
          }),
          submitted && fr && !fr.ok
            ? React.createElement("div", { style: { padding: "0 8px 4px", fontSize: "8px", color: "#52a366" } }, "\u2713 " + fr.correct)
            : null
        );
      })()));
    })));
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid #1a1c18",
      marginBottom: "12px",
      background: "#0d100b",
      opacity: 0.5
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "5px 10px",
      borderBottom: "1px solid #1a1c18"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, "Post-Assembly Section ", /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "8px",
      color: "#3a3d37"
    }
  }, "(completed after physical assembly \u2014 not part of this exercise)"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr 1fr"
    }
  }, [["Achieved Torque (ft-lb)", ""], ["Assembly Date", ""], ["Inspector Initials", ""], ["Result (ACC/REJ)", ""]].map(function (_ref0, i) {
    var _ref1 = _slicedToArray(_ref0, 1),
      l = _ref1[0];
    return /*#__PURE__*/React.createElement("div", {
      key: l,
      style: {
        padding: "6px 10px",
        borderRight: i < 3 ? "1px solid #1a1c18" : "none"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#3a3d37",
        fontSize: "7px",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        marginBottom: "2px"
      }
    }, l), /*#__PURE__*/React.createElement("div", {
      style: {
        height: "20px",
        background: "#0a0b09",
        border: "1px solid #1a1c18"
      }
    }));
  }))), !submitted && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "8px"
    }
  }, allFilled ? "All fields complete — ready to submit." : "Complete all fields to submit."), /*#__PURE__*/React.createElement("button", {
    onClick: handleSubmit,
    disabled: !allFilled,
    style: {
      background: allFilled ? amber : "#232520",
      color: allFilled ? bg : "#3d3f39",
      border: "none",
      padding: "10px 22px",
      cursor: allFilled ? "pointer" : "not-allowed",
      fontFamily: mono,
      fontSize: "11px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      fontWeight: 600
    }
  }, "Submit Pre-Assembly Forms")));
}

// ── ISO MAP ───────────────────────────────────────────────────
function IsoMap() {
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 920 638",
    width: "100%",
    style: {
      display: "block",
      fontFamily: "IBM Plex Mono, monospace"
    }
  }, /*#__PURE__*/React.createElement("rect", {
    width: "920",
    height: "490",
    fill: "#0a0b09"
  }), /*#__PURE__*/React.createElement("g", {
    stroke: "#1e211a",
    strokeWidth: "0.6",
    strokeDasharray: "3,9"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "270",
    x2: "468",
    y2: "0"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "420",
    x2: "728",
    y2: "0"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "173",
    y1: "490",
    x2: "920",
    y2: "49"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "381",
    y1: "490",
    x2: "920",
    y2: "169"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "588",
    y1: "490",
    x2: "920",
    y2: "298"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "50",
    x2: "745",
    y2: "490"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "250",
    x2: "399",
    y2: "490"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "347",
    y1: "0",
    x2: "920",
    y2: "331"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "693",
    y1: "0",
    x2: "920",
    y2: "131"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "230",
    y1: "0",
    x2: "230",
    y2: "490"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "460",
    y1: "0",
    x2: "460",
    y2: "490"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "690",
    y1: "0",
    x2: "690",
    y2: "490"
  })), /*#__PURE__*/React.createElement("polygon", {
    points: "10,375 72,340 72,415 10,450",
    fill: "#0f1812",
    stroke: "#1e3828",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "10",
    y1: "413",
    x2: "72",
    y2: "378",
    stroke: "#1c3024",
    strokeWidth: "0.8",
    strokeDasharray: "4,4"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "10",
    y1: "432",
    x2: "72",
    y2: "397",
    stroke: "#1c3024",
    strokeWidth: "0.8",
    strokeDasharray: "4,4"
  }), /*#__PURE__*/React.createElement("text", {
    x: "24",
    y: "393",
    fill: "#2d5240",
    fontSize: "8",
    fontWeight: "700",
    letterSpacing: "0.1em"
  }, "COMP-A"), /*#__PURE__*/React.createElement("text", {
    x: "24",
    y: "404",
    fill: "#233d30",
    fontSize: "7"
  }, "TRAIN A"), /*#__PURE__*/React.createElement("line", {
    x1: "72",
    y1: "390",
    x2: "80",
    y2: "390",
    stroke: "#3a556a",
    strokeWidth: "6"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "710",
    y1: "60",
    x2: "742",
    y2: "43",
    stroke: "#3a556a",
    strokeWidth: "6"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "745",
    y: "24",
    width: "35",
    height: "22",
    fill: "#0f1812",
    stroke: "#1e3828",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "763",
    y: "38",
    textAnchor: "middle",
    fill: "#2d5240",
    fontSize: "7",
    fontWeight: "700"
  }, "DISCH."), /*#__PURE__*/React.createElement("text", {
    x: "763",
    y: "47",
    textAnchor: "middle",
    fill: "#233d30",
    fontSize: "6"
  }, "HDR."), /*#__PURE__*/React.createElement("line", {
    x1: "83.5",
    y1: "426",
    x2: "713.5",
    y2: "66",
    stroke: "#253545",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "76.5",
    y1: "414",
    x2: "706.5",
    y2: "54",
    stroke: "#253545",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "80",
    y1: "420",
    x2: "710",
    y2: "60",
    stroke: "#3a556a",
    strokeWidth: "5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "80",
    y1: "420",
    x2: "710",
    y2: "60",
    stroke: "#4e7490",
    strokeWidth: "2",
    opacity: "0.25"
  }), /*#__PURE__*/React.createElement("text", {
    transform: "translate(230,337) rotate(-30)",
    fill: "#2a4252",
    fontSize: "7.5",
    letterSpacing: "0.08em"
  }, "6\" \xB7 A106-B \xB7 P600 \xB7 SOUR SVC"), /*#__PURE__*/React.createElement("line", {
    x1: "326",
    y1: "276",
    x2: "326",
    y2: "182",
    stroke: "#253545",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "338",
    y1: "276",
    x2: "338",
    y2: "182",
    stroke: "#253545",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "332",
    y1: "276",
    x2: "332",
    y2: "182",
    stroke: "#3a556a",
    strokeWidth: "4"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "332",
    y1: "276",
    x2: "332",
    y2: "182",
    stroke: "#4e7490",
    strokeWidth: "1.5",
    opacity: "0.25"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "322",
    y1: "182",
    x2: "342",
    y2: "182",
    stroke: "#2a4a5a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "322",
    y1: "174",
    x2: "322",
    y2: "182",
    stroke: "#2a4a5a",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "342",
    y1: "174",
    x2: "342",
    y2: "182",
    stroke: "#2a4a5a",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "348",
    y: "180",
    fill: "#3a5a68",
    fontSize: "7.5"
  }, "TO RECYCLE HDR."), /*#__PURE__*/React.createElement("text", {
    x: "348",
    y: "190",
    fill: "#2a4050",
    fontSize: "7"
  }, "4\" \xB7 P600"), /*#__PURE__*/React.createElement("line", {
    x1: "454",
    y1: "204",
    x2: "454",
    y2: "318",
    stroke: "#253545",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "462",
    y1: "204",
    x2: "462",
    y2: "318",
    stroke: "#253545",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "458",
    y1: "204",
    x2: "458",
    y2: "318",
    stroke: "#3a556a",
    strokeWidth: "4"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "458",
    y1: "204",
    x2: "458",
    y2: "318",
    stroke: "#4e7490",
    strokeWidth: "1.5",
    opacity: "0.25"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "446,312 470,312 458,324",
    fill: "none",
    stroke: "#3a6a7a",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "446,324 470,324 458,312",
    fill: "none",
    stroke: "#3a6a7a",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "446",
    y1: "318",
    x2: "441",
    y2: "318",
    stroke: "#2a4a5a",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "470",
    y1: "318",
    x2: "475",
    y2: "318",
    stroke: "#2a4a5a",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "448",
    y: "330",
    width: "20",
    height: "12",
    fill: "#0f1218",
    stroke: "#2a4050",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("text", {
    x: "458",
    y: "340",
    textAnchor: "middle",
    fill: "#3a5a68",
    fontSize: "6",
    fontWeight: "700"
  }, "PSV"), /*#__PURE__*/React.createElement("text", {
    x: "482",
    y: "322",
    fill: "#3a5a68",
    fontSize: "7.5"
  }, "PSV-101"), /*#__PURE__*/React.createElement("text", {
    x: "482",
    y: "332",
    fill: "#2a4050",
    fontSize: "7"
  }, "3\" \xB7 P600"), /*#__PURE__*/React.createElement("line", {
    x1: "618",
    y1: "111",
    x2: "618",
    y2: "52",
    stroke: "#253545",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "624",
    y1: "111",
    x2: "624",
    y2: "52",
    stroke: "#253545",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "621",
    y1: "111",
    x2: "621",
    y2: "52",
    stroke: "#3a556a",
    strokeWidth: "3"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "621",
    y1: "111",
    x2: "621",
    y2: "52",
    stroke: "#4e7490",
    strokeWidth: "1.2",
    opacity: "0.25"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "614",
    y1: "52",
    x2: "628",
    y2: "52",
    stroke: "#3a6a7a",
    strokeWidth: "3"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "614",
    y: "44",
    width: "14",
    height: "8",
    fill: "#1a2a34",
    stroke: "#2a5060",
    strokeWidth: "1"
  }), /*#__PURE__*/React.createElement("text", {
    x: "631",
    y: "55",
    fill: "#3a5a68",
    fontSize: "7.5"
  }, "DRAIN"), /*#__PURE__*/React.createElement("text", {
    x: "631",
    y: "64",
    fill: "#2a4050",
    fontSize: "7"
  }, "1.5\" \xB7 P600"), /*#__PURE__*/React.createElement("polygon", {
    points: "216,342 197,349 202,356",
    fill: "#d4832a",
    opacity: "0.55"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "549,152 530,159 535,166",
    fill: "#d4832a",
    opacity: "0.55"
  }), /*#__PURE__*/React.createElement("g", {
    transform: "translate(80,420) rotate(-30)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-4.5",
    y1: "-20",
    x2: "-4.5",
    y2: "20",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "4.5",
    y1: "-20",
    x2: "4.5",
    y2: "20",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "0",
    cy: "-14",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "0",
    cy: "14",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "-14",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "14",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  })), /*#__PURE__*/React.createElement("g", {
    transform: "translate(710,60) rotate(-30)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-4.5",
    y1: "-20",
    x2: "-4.5",
    y2: "20",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "4.5",
    y1: "-20",
    x2: "4.5",
    y2: "20",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "0",
    cy: "-14",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "0",
    cy: "14",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "-14",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "14",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  })), /*#__PURE__*/React.createElement("g", {
    transform: "translate(332,225)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-18",
    y1: "-4.5",
    x2: "18",
    y2: "-4.5",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "-18",
    y1: "4.5",
    x2: "18",
    y2: "4.5",
    stroke: "#d4832a",
    strokeWidth: "2.5"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "-12",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "0",
    r: "2",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  })), /*#__PURE__*/React.createElement("g", {
    transform: "translate(458,265)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-16",
    y1: "-4.5",
    x2: "16",
    y2: "-4.5",
    stroke: "#d4832a",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "-16",
    y1: "4.5",
    x2: "16",
    y2: "4.5",
    stroke: "#d4832a",
    strokeWidth: "2"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "-10",
    cy: "0",
    r: "1.5",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "10",
    cy: "0",
    r: "1.5",
    fill: "none",
    stroke: "#d4832a",
    strokeWidth: "1",
    opacity: "0.6"
  })), /*#__PURE__*/React.createElement("g", {
    transform: "translate(621,82)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-12",
    y1: "-3.5",
    x2: "12",
    y2: "-3.5",
    stroke: "#d4832a",
    strokeWidth: "1.8"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "-12",
    y1: "3.5",
    x2: "12",
    y2: "3.5",
    stroke: "#d4832a",
    strokeWidth: "1.8"
  })), /*#__PURE__*/React.createElement("line", {
    x1: "80",
    y1: "416",
    x2: "82",
    y2: "340",
    stroke: "#d4832a",
    strokeWidth: "0.8",
    strokeDasharray: "4,4",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "82,340 78,352 86,352",
    fill: "#d4832a",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "14",
    y: "262",
    width: "130",
    height: "72",
    fill: "#080d0a",
    stroke: "#d4832a",
    strokeWidth: "1",
    rx: "1"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "14",
    y: "262",
    width: "130",
    height: "15",
    fill: "rgba(212,131,42,0.15)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "14",
    y1: "277",
    x2: "144",
    y2: "277",
    stroke: "#d4832a",
    strokeWidth: "0.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "20",
    y: "273",
    fill: "#d4832a",
    fontSize: "8.5",
    fontWeight: "700"
  }, "FLG-001 \xB7 6\" CL600"), /*#__PURE__*/React.createElement("text", {
    x: "20",
    y: "289",
    fill: "#ede8df",
    fontSize: "9.5"
  }, "TQ: 185 ft-lb"), /*#__PURE__*/React.createElement("text", {
    x: "20",
    y: "302",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "Cross \xB7 3-pass"), /*#__PURE__*/React.createElement("text", {
    x: "20",
    y: "315",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "A193 B7 / A194 2H"), /*#__PURE__*/React.createElement("text", {
    x: "20",
    y: "328",
    fill: "#5e5b53",
    fontSize: "7"
  }, "SUCT. NOZZLE N1"), /*#__PURE__*/React.createElement("line", {
    x1: "712",
    y1: "57",
    x2: "730",
    y2: "70",
    stroke: "#d4832a",
    strokeWidth: "0.8",
    strokeDasharray: "4,4",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "730,70 720,62 726,74",
    fill: "#d4832a",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "730",
    y: "34",
    width: "130",
    height: "72",
    fill: "#080d0a",
    stroke: "#d4832a",
    strokeWidth: "1",
    rx: "1"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "730",
    y: "34",
    width: "130",
    height: "15",
    fill: "rgba(212,131,42,0.15)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "730",
    y1: "49",
    x2: "860",
    y2: "49",
    stroke: "#d4832a",
    strokeWidth: "0.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "736",
    y: "45",
    fill: "#d4832a",
    fontSize: "8.5",
    fontWeight: "700"
  }, "FLG-002 \xB7 6\" CL600"), /*#__PURE__*/React.createElement("text", {
    x: "736",
    y: "61",
    fill: "#ede8df",
    fontSize: "9.5"
  }, "TQ: 185 ft-lb"), /*#__PURE__*/React.createElement("text", {
    x: "736",
    y: "74",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "Cross \xB7 3-pass"), /*#__PURE__*/React.createElement("text", {
    x: "736",
    y: "87",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "A193 B7 / A194 2H"), /*#__PURE__*/React.createElement("text", {
    x: "736",
    y: "100",
    fill: "#5e5b53",
    fontSize: "7"
  }, "DISCH. NOZZLE N2"), /*#__PURE__*/React.createElement("line", {
    x1: "334",
    y1: "218",
    x2: "358",
    y2: "175",
    stroke: "#d4832a",
    strokeWidth: "0.8",
    strokeDasharray: "4,4",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "358,175 350,184 363,186",
    fill: "#d4832a",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "356",
    y: "97",
    width: "130",
    height: "72",
    fill: "#080d0a",
    stroke: "#d4832a",
    strokeWidth: "1",
    rx: "1"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "356",
    y: "97",
    width: "130",
    height: "15",
    fill: "rgba(212,131,42,0.15)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "356",
    y1: "112",
    x2: "486",
    y2: "112",
    stroke: "#d4832a",
    strokeWidth: "0.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "362",
    y: "108",
    fill: "#d4832a",
    fontSize: "8.5",
    fontWeight: "700"
  }, "FLG-003 \xB7 4\" CL600"), /*#__PURE__*/React.createElement("text", {
    x: "362",
    y: "124",
    fill: "#ede8df",
    fontSize: "9.5"
  }, "TQ: 120 ft-lb"), /*#__PURE__*/React.createElement("text", {
    x: "362",
    y: "137",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "Cross \xB7 3-pass"), /*#__PURE__*/React.createElement("text", {
    x: "362",
    y: "150",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "A193 B7 / A194 2H"), /*#__PURE__*/React.createElement("text", {
    x: "362",
    y: "163",
    fill: "#5e5b53",
    fontSize: "7"
  }, "RECYCLE TIE-IN"), /*#__PURE__*/React.createElement("line", {
    x1: "460",
    y1: "271",
    x2: "498",
    y2: "297",
    stroke: "#d4832a",
    strokeWidth: "0.8",
    strokeDasharray: "4,4",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "498,297 486,287 491,300",
    fill: "#d4832a",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "496",
    y: "282",
    width: "130",
    height: "72",
    fill: "#080d0a",
    stroke: "#d4832a",
    strokeWidth: "1",
    rx: "1"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "496",
    y: "282",
    width: "130",
    height: "15",
    fill: "rgba(212,131,42,0.15)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "496",
    y1: "297",
    x2: "626",
    y2: "297",
    stroke: "#d4832a",
    strokeWidth: "0.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "502",
    y: "293",
    fill: "#d4832a",
    fontSize: "8.5",
    fontWeight: "700"
  }, "FLG-004 \xB7 3\" CL600"), /*#__PURE__*/React.createElement("text", {
    x: "502",
    y: "309",
    fill: "#ede8df",
    fontSize: "9.5"
  }, "TQ: 120 ft-lb"), /*#__PURE__*/React.createElement("text", {
    x: "502",
    y: "322",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "Cross \xB7 3-pass"), /*#__PURE__*/React.createElement("text", {
    x: "502",
    y: "335",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "A193 B7 / A194 2H"), /*#__PURE__*/React.createElement("text", {
    x: "502",
    y: "348",
    fill: "#5e5b53",
    fontSize: "7"
  }, "PSV-101 INLET"), /*#__PURE__*/React.createElement("line", {
    x1: "622",
    y1: "78",
    x2: "650",
    y2: "135",
    stroke: "#d4832a",
    strokeWidth: "0.8",
    strokeDasharray: "4,4",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("polygon", {
    points: "650,135 640,126 647,137",
    fill: "#d4832a",
    opacity: "0.65"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "642",
    y: "128",
    width: "130",
    height: "72",
    fill: "#080d0a",
    stroke: "#d4832a",
    strokeWidth: "1",
    rx: "1"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "642",
    y: "128",
    width: "130",
    height: "15",
    fill: "rgba(212,131,42,0.15)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "642",
    y1: "143",
    x2: "772",
    y2: "143",
    stroke: "#d4832a",
    strokeWidth: "0.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "648",
    y: "139",
    fill: "#d4832a",
    fontSize: "8.5",
    fontWeight: "700"
  }, "FLG-005 \xB7 1.5\" CL600"), /*#__PURE__*/React.createElement("text", {
    x: "648",
    y: "155",
    fill: "#ede8df",
    fontSize: "9.5"
  }, "TQ: 65 ft-lb"), /*#__PURE__*/React.createElement("text", {
    x: "648",
    y: "168",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "Cross \xB7 2-pass"), /*#__PURE__*/React.createElement("text", {
    x: "648",
    y: "181",
    fill: "#ccc8be",
    fontSize: "8.5"
  }, "A193 B7 / A194 2H"), /*#__PURE__*/React.createElement("text", {
    x: "648",
    y: "194",
    fill: "#5e5b53",
    fontSize: "7"
  }, "DRAIN CONN."), /*#__PURE__*/React.createElement("circle", {
    cx: "80",
    cy: "420",
    r: "9",
    fill: "#0a0b09",
    stroke: "#d4832a",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "80",
    y: "424",
    textAnchor: "middle",
    fill: "#d4832a",
    fontSize: "6",
    fontWeight: "700"
  }, "001"), /*#__PURE__*/React.createElement("circle", {
    cx: "710",
    cy: "60",
    r: "9",
    fill: "#0a0b09",
    stroke: "#d4832a",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "710",
    y: "64",
    textAnchor: "middle",
    fill: "#d4832a",
    fontSize: "6",
    fontWeight: "700"
  }, "002"), /*#__PURE__*/React.createElement("circle", {
    cx: "332",
    cy: "225",
    r: "8",
    fill: "#0a0b09",
    stroke: "#d4832a",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "332",
    y: "229",
    textAnchor: "middle",
    fill: "#d4832a",
    fontSize: "6",
    fontWeight: "700"
  }, "003"), /*#__PURE__*/React.createElement("circle", {
    cx: "458",
    cy: "265",
    r: "8",
    fill: "#0a0b09",
    stroke: "#d4832a",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "458",
    y: "269",
    textAnchor: "middle",
    fill: "#d4832a",
    fontSize: "6",
    fontWeight: "700"
  }, "004"), /*#__PURE__*/React.createElement("circle", {
    cx: "621",
    cy: "82",
    r: "7",
    fill: "#0a0b09",
    stroke: "#d4832a",
    strokeWidth: "1.2"
  }), /*#__PURE__*/React.createElement("text", {
    x: "621",
    y: "86",
    textAnchor: "middle",
    fill: "#d4832a",
    fontSize: "6",
    fontWeight: "700"
  }, "005"), /*#__PURE__*/React.createElement("g", {
    transform: "translate(856,445)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "0",
    x2: "20",
    y2: "-10",
    stroke: "#3a5060",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "0",
    x2: "-20",
    y2: "-10",
    stroke: "#3a5060",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "-22",
    stroke: "#3a5060",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("text", {
    x: "24",
    y: "-8",
    fill: "#3a5060",
    fontSize: "7"
  }, "E"), /*#__PURE__*/React.createElement("text", {
    x: "-32",
    y: "-8",
    fill: "#3a5060",
    fontSize: "7"
  }, "N"), /*#__PURE__*/React.createElement("text", {
    x: "2",
    y: "-24",
    fill: "#3a5060",
    fontSize: "7"
  }, "U")), /*#__PURE__*/React.createElement("rect", {
    x: "10",
    y: "464",
    width: "200",
    height: "20",
    fill: "#080d0a",
    stroke: "#1e211a",
    strokeWidth: "0.8"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "18",
    y1: "474",
    x2: "40",
    y2: "474",
    stroke: "#3a556a",
    strokeWidth: "4"
  }), /*#__PURE__*/React.createElement("text", {
    x: "44",
    y: "477",
    fill: "#4a5a62",
    fontSize: "7"
  }, "Pipe"), /*#__PURE__*/React.createElement("g", {
    transform: "translate(108,474)"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "-8",
    y1: "-6",
    x2: "8",
    y2: "-6",
    stroke: "#d4832a",
    strokeWidth: "1.8"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "-8",
    y1: "6",
    x2: "8",
    y2: "6",
    stroke: "#d4832a",
    strokeWidth: "1.8"
  })), /*#__PURE__*/React.createElement("text", {
    x: "120",
    y: "477",
    fill: "#4a5a62",
    fontSize: "7"
  }, "Flange"), /*#__PURE__*/React.createElement("polygon", {
    points: "82,470 70,474 73,478",
    fill: "#d4832a",
    opacity: "0.6"
  }), /*#__PURE__*/React.createElement("text", {
    x: "86",
    y: "477",
    fill: "#4a5a62",
    fontSize: "7"
  }, "Flow"), /*#__PURE__*/React.createElement("line", {
    x1: "1",
    y1: "492",
    x2: "919",
    y2: "492",
    stroke: "#2a3d2a",
    strokeWidth: "1.5"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "1",
    y: "492",
    width: "918",
    height: "145",
    fill: "#080c07"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "1",
    y: "492",
    width: "918",
    height: "14",
    fill: "rgba(212,131,42,0.1)"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "1",
    y1: "506",
    x2: "919",
    y2: "506",
    stroke: "#2a2d27",
    strokeWidth: "0.8"
  }), /*#__PURE__*/React.createElement("text", {
    x: "8",
    y: "502",
    fill: "#d4832a",
    fontSize: "8",
    fontWeight: "700",
    letterSpacing: "0.2em"
  }, "BILL OF MATERIALS"), /*#__PURE__*/React.createElement("text", {
    x: "580",
    y: "502",
    fill: "#3a5060",
    fontSize: "7",
    letterSpacing: "0.1em"
  }, "PROJ: MUSTANG CREEK COMPRESSOR STATION  \xB7  SYS: DISCH. PIPING TRAIN A  \xB7  SPEC: Q-SPEC-2200 REV.3"), /*#__PURE__*/React.createElement("rect", {
    x: "1",
    y: "506",
    width: "918",
    height: "13",
    fill: "#121610"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "1",
    y1: "519",
    x2: "919",
    y2: "519",
    stroke: "#2a2d27",
    strokeWidth: "0.8"
  }), ["ITM", "QTY", "DESCRIPTION", "MATERIAL / SPEC", "HEAT NO.", "CERT / LOT NO."].map(function (h, i) {
    var xs = [8, 34, 62, 438, 662, 790];
    return /*#__PURE__*/React.createElement("text", {
      key: i,
      x: xs[i],
      y: 516,
      fill: "#6e6b63",
      fontSize: "6.5",
      fontWeight: "700",
      letterSpacing: "0.1em",
      textAnchor: "start"
    }, h);
  }), [30, 58, 434, 658, 786].map(function (x) {
    return /*#__PURE__*/React.createElement("line", {
      key: x,
      x1: x,
      y1: "492",
      x2: x,
      y2: "637",
      stroke: "#2a2d27",
      strokeWidth: "0.6"
    });
  }), [["1", "2", '6" 600# WN Flange RF, ASME B16.5', "ASTM A105N", "HT-3821A", "MTR-6612"], ["2", "1", '4" 600# WN Flange RF, ASME B16.5', "ASTM A105N", "HT-3821A", "MTR-6612"], ["3", "1", '3" 600# WN Flange RF, ASME B16.5', "ASTM A105N", "HT-3821B", "MTR-6613"], ["4", "1", '1.5" 600# WN Flange RF, ASME B16.5', "ASTM A105N", "HT-3821B", "MTR-6613"], ["5", "5", 'SWG 316SS/Flex Graphite, ASME B16.20', "316SS/Flex Graphite", "—", "GT-2241"], ["6", "32", 'Stud Bolt 1"×7.25" (6" 600#)', "ASTM A193 B7", "HT-9042", "MTR-8801"], ["7", "16", 'Stud Bolt 7/8"×6.25" (4" 600#)', "ASTM A193 B7", "HT-9042", "MTR-8801"], ["8", "12", 'Stud Bolt 3/4"×5.75" (3" 600#)', "ASTM A193 B7", "HT-9042", "MTR-8801"], ["9", "8", 'Stud Bolt 5/8"×4.50" (1.5" 600#)', "ASTM A193 B7", "HT-9042", "MTR-8801"], ["10", "64", "Heavy Hex Nut (all sizes)", "ASTM A194 2H", "HT-9043", "MTR-8802"]].map(function (row, i) {
    var y = 519 + i * 12;
    var even = i % 2 === 0;
    var xs = [8, 34, 62, 438, 662, 790];
    var colors = ["#d4832a", "#ede8df", "#ede8df", "#ccc8be", "#6e6b63", "#52a366"];
    return /*#__PURE__*/React.createElement("g", {
      key: i
    }, !even && /*#__PURE__*/React.createElement("rect", {
      x: "2",
      y: y,
      width: "916",
      height: "12",
      fill: "rgba(255,255,255,0.015)"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "2",
      y1: y + 12,
      x2: "918",
      y2: y + 12,
      stroke: "#1e211a",
      strokeWidth: "0.5"
    }), row.map(function (val, ci) {
      return /*#__PURE__*/React.createElement("text", {
        key: ci,
        x: xs[ci] + (ci === 0 || ci === 1 ? 0 : 0),
        y: y + 9,
        fill: colors[ci],
        fontSize: "7.5",
        fontFamily: "IBM Plex Mono",
        textAnchor: "start",
        fontWeight: ci <= 1 ? "700" : "400"
      }, val);
    }));
  }), /*#__PURE__*/React.createElement("rect", {
    x: "1",
    y: "1",
    width: "918",
    height: "636",
    fill: "none",
    stroke: "#1e211a",
    strokeWidth: "1"
  }));
}

// ── TABLE CELL STYLES ─────────────────────────────────────────
var th = function th() {
  var x = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  return _objectSpread({
    padding: "6px 8px",
    textAlign: "left",
    color: amber,
    fontSize: "8px",
    letterSpacing: "0.1em",
    textTransform: "uppercase",
    borderBottom: "1px solid ".concat(border),
    fontWeight: 700,
    whiteSpace: "nowrap",
    background: surf2
  }, x);
};
var td = function td() {
  var x = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};
  return _objectSpread({
    padding: "6px 8px",
    color: textCol,
    fontSize: "10px",
    borderBottom: "1px solid ".concat(border),
    verticalAlign: "top"
  }, x);
};

// ── JOINT TORQUE FORM ─────────────────────────────────────────
function JointForm(_ref10) {
  var f = _ref10.f;
  var Row = function Row(_ref11) {
    var label = _ref11.label,
      value = _ref11.value,
      _ref11$hi = _ref11.hi,
      hi = _ref11$hi === void 0 ? false : _ref11$hi,
      _ref11$accent = _ref11.accent,
      accent = _ref11$accent === void 0 ? false : _ref11$accent;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        borderBottom: "1px solid ".concat(border),
        minHeight: "26px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: "148px",
        flexShrink: 0,
        padding: "5px 8px",
        background: surf2,
        color: textCol,
        fontSize: "8px",
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        borderRight: "1px solid ".concat(border),
        display: "flex",
        alignItems: "center"
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1,
        padding: "5px 8px",
        color: accent ? amber : hi ? white : textCol,
        fontSize: hi ? "12px" : "10px",
        fontWeight: hi ? 700 : 400,
        display: "flex",
        alignItems: "center"
      }
    }, value));
  };
  var Divider = function Divider(_ref12) {
    var label = _ref12.label;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "5px 8px",
        background: "rgba(212,131,42,0.07)",
        borderBottom: "1px solid ".concat(border),
        borderTop: "1px solid ".concat(border),
        color: amber,
        fontSize: "7.5px",
        letterSpacing: "0.16em",
        textTransform: "uppercase",
        marginTop: "2px"
      }
    }, label);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      border: "1px solid ".concat(border),
      background: surf
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(212,131,42,0.12)",
      borderBottom: "2px solid ".concat(amber),
      padding: "8px 12px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "11px",
      fontWeight: 700,
      letterSpacing: "0.06em"
    }
  }, f.id, " \u2014 ", f.location), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      marginTop: "2px"
    }
  }, f.size, " \xB7 ", f.cls, " \xB7 ", SCENARIO.system, " \xB7 ", SCENARIO.spec)), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "9px",
      color: muted,
      letterSpacing: "0.1em",
      textTransform: "uppercase"
    }
  }, "Result"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "16px",
      fontWeight: 900,
      color: f.result === "ACC" ? green : red,
      letterSpacing: "0.08em"
    }
  }, f.result))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr",
      borderBottom: "1px solid ".concat(border)
    }
  }, [["Target", f.targetTorque + " ft-lb", amber], ["Snug Pass", f.snugTorque + " ft-lb", "#8ab4c4"], ["Mid Pass", f.midTorque + " ft-lb", "#8ab4c4"], ["Final Pass", f.finalTorque + " ft-lb", amber], ["Achieved", f.achievedTorque + " ft-lb", green]].map(function (_ref13) {
    var _ref14 = _slicedToArray(_ref13, 3),
      label = _ref14[0],
      val = _ref14[1],
      color = _ref14[2];
    return /*#__PURE__*/React.createElement("div", {
      key: label,
      style: {
        padding: "8px 10px",
        borderRight: "1px solid ".concat(border),
        textAlign: "center"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: muted,
        fontSize: "7px",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        marginBottom: "3px"
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        color: color,
        fontSize: "13px",
        fontWeight: 700
      }
    }, val));
  })), /*#__PURE__*/React.createElement(Divider, {
    label: "Bolt & Nut Data"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Size / Length",
    value: f.boltSize,
    hi: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Qty",
    value: f.boltQty + " bolts"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Material",
    value: f.boltMat
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Heat No.",
    value: f.boltHeat
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Cert No.",
    value: f.boltCert,
    accent: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Nut Material",
    value: f.nutMat
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Nut Cert No.",
    value: f.nutCert,
    accent: true
  }), /*#__PURE__*/React.createElement(Divider, {
    label: "Gasket Data"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Gasket Type",
    value: f.gasketType,
    hi: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Gasket Std",
    value: f.gasketStd
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Gasket Lot #",
    value: f.gasketLot,
    accent: true
  }), /*#__PURE__*/React.createElement(Divider, {
    label: "Flange Data"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Flange Material",
    value: f.flangeMat
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Flange Heat No.",
    value: f.flangeHeat
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Flange Cert No.",
    value: f.flangeCert,
    accent: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Surface Finish",
    value: f.surfaceFinish
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Alignment Check",
    value: f.alignmentCheck,
    hi: true
  }), /*#__PURE__*/React.createElement(Divider, {
    label: "Installation"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Lubricant",
    value: f.lubricant
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Bolt Engagement",
    value: f.boltEngagement
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Pattern",
    value: f.pattern,
    hi: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Passes",
    value: f.passes,
    hi: true
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Gasket Condition",
    value: f.gasketCondition
  }), /*#__PURE__*/React.createElement(Divider, {
    label: "Inspection Record"
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Date",
    value: f.date
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Shift",
    value: f.shift
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Torque Wrench ID",
    value: f.wrenchId
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Wrench Cal. Due",
    value: f.wrenchCalDue
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Inspector",
    value: f.inspector
  }), /*#__PURE__*/React.createElement(Row, {
    label: "Initials",
    value: f.initials,
    hi: true,
    accent: true
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "8px 10px",
      borderTop: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      marginBottom: "4px"
    }
  }, "Remarks"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: textCol,
      fontSize: "10px",
      lineHeight: 1.6
    }
  }, f.remarks)));
}

// ── COMPANY SPECIFICATION DOCUMENT ───────────────────────────
function SpecDocument() {
  var sans = "'IBM Plex Mono', monospace";
  var DocHeader = function DocHeader() {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        background: "#080d0a",
        border: "1px solid ".concat(border),
        marginBottom: "0"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        height: "3px",
        background: "linear-gradient(90deg, ".concat(amber, ", #3a5060)")
      }
    }), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "grid",
        gridTemplateColumns: "1fr auto",
        borderBottom: "1px solid ".concat(border)
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "10px 14px",
        borderRight: "1px solid ".concat(border)
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#4a6a52",
        fontSize: "8px",
        letterSpacing: "0.22em",
        textTransform: "uppercase",
        marginBottom: "4px"
      }
    }, "Mustang Energy Partners, LLC"), /*#__PURE__*/React.createElement("div", {
      style: {
        color: white,
        fontSize: "13px",
        fontWeight: 700,
        letterSpacing: "0.04em"
      }
    }, "PIPING SPECIFICATION"), /*#__PURE__*/React.createElement("div", {
      style: {
        color: amber,
        fontSize: "10px",
        letterSpacing: "0.08em",
        marginTop: "2px"
      }
    }, "Bolted Flange Assembly & Torque Control")), /*#__PURE__*/React.createElement("div", {
      style: {
        padding: "8px 14px",
        display: "grid",
        gridTemplateColumns: "auto auto",
        gap: "0",
        minWidth: "280px"
      }
    }, [["Document No.", "MEP-PIP-SPEC-044"], ["Revision", "3"], ["Issue Date", "2024-11-15"], ["Supersedes", "Rev. 2 (2022-06-01)"], ["Status", "APPROVED — FOR CONSTRUCTION"], ["Applies To", "Class 600 & Below, All Services"]].map(function (_ref15, i) {
      var _ref16 = _slicedToArray(_ref15, 2),
        l = _ref16[0],
        v = _ref16[1];
      return /*#__PURE__*/React.createElement(React.Fragment, {
        key: l
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          padding: "3px 8px 3px 0",
          borderBottom: "1px solid ".concat(border),
          color: muted,
          fontSize: "7.5px",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          paddingRight: "12px",
          borderRight: "1px solid ".concat(border)
        }
      }, l), /*#__PURE__*/React.createElement("div", {
        style: {
          padding: "3px 0 3px 10px",
          borderBottom: "1px solid ".concat(border),
          color: v.includes("APPROVED") ? green : v === "3" ? amber : textCol,
          fontSize: "8px",
          fontWeight: v === "3" || v.includes("APPROVED") ? "700" : "400"
        }
      }, v));
    }))), /*#__PURE__*/React.createElement("div", {
      style: {
        display: "grid",
        gridTemplateColumns: "1fr 1fr 1fr 1fr",
        borderBottom: "1px solid ".concat(border)
      }
    }, [["Prepared By", "T. Okafor / Piping Eng.", "2024-11-08"], ["Reviewed By", "K. Duke / Sr. Eng.", "2024-11-10"], ["Approved By", "M. McDougall / Proj. Dir.", "2024-11-15"], ["QC Authority", "B. Hayes / QC Dir.", "2024-11-15"]].map(function (_ref17, i) {
      var _ref18 = _slicedToArray(_ref17, 3),
        role = _ref18[0],
        name = _ref18[1],
        date = _ref18[2];
      return /*#__PURE__*/React.createElement("div", {
        key: role,
        style: {
          padding: "6px 10px",
          borderRight: i < 3 ? "1px solid ".concat(border) : "none"
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          color: muted,
          fontSize: "7px",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          marginBottom: "2px"
        }
      }, role), /*#__PURE__*/React.createElement("div", {
        style: {
          color: white,
          fontSize: "8.5px"
        }
      }, name), /*#__PURE__*/React.createElement("div", {
        style: {
          color: muted,
          fontSize: "7.5px",
          marginTop: "1px"
        }
      }, date));
    })));
  };
  var Section = function Section(_ref19) {
    var num = _ref19.num,
      title = _ref19.title,
      children = _ref19.children;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        marginBottom: "14px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        padding: "6px 10px",
        background: "rgba(212,131,42,0.07)",
        borderLeft: "2px solid ".concat(amber),
        borderBottom: "1px solid ".concat(border),
        marginBottom: "0"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: amber,
        fontSize: "9px",
        fontWeight: 700,
        letterSpacing: "0.14em",
        minWidth: "28px"
      }
    }, num), /*#__PURE__*/React.createElement("span", {
      style: {
        color: white,
        fontSize: "9.5px",
        fontWeight: 700,
        letterSpacing: "0.06em",
        textTransform: "uppercase"
      }
    }, title)), /*#__PURE__*/React.createElement("div", {
      style: {
        border: "1px solid ".concat(border),
        borderTop: "none",
        padding: "10px 12px",
        background: surf
      }
    }, children));
  };
  var Clause = function Clause(_ref20) {
    var id = _ref20.id,
      children = _ref20.children,
      _ref20$warn = _ref20.warn,
      warn = _ref20$warn === void 0 ? false : _ref20$warn,
      _ref20$note = _ref20.note,
      note = _ref20$note === void 0 ? false : _ref20$note;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        gap: "10px",
        marginBottom: "7px",
        paddingBottom: "7px",
        borderBottom: "1px solid #1a1c18"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: warn ? "#c95f5f" : note ? "#8ab4c4" : muted,
        fontSize: "8px",
        fontWeight: 700,
        minWidth: "36px",
        paddingTop: "1px",
        flexShrink: 0,
        letterSpacing: "0.06em"
      }
    }, id), /*#__PURE__*/React.createElement("span", {
      style: {
        color: warn ? "#e8b4b0" : note ? "#b4ccd4" : textCol,
        fontSize: "10px",
        lineHeight: 1.65,
        fontStyle: note ? "italic" : "normal"
      }
    }, children));
  };
  var TableNote = function TableNote(_ref21) {
    var children = _ref21.children;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#8ab4c4",
        fontSize: "8.5px",
        fontStyle: "italic",
        marginTop: "5px",
        lineHeight: 1.5,
        paddingLeft: "4px",
        borderLeft: "1px solid #2a4050"
      }
    }, children);
  };
  var Warn = function Warn(_ref22) {
    var children = _ref22.children;
    return /*#__PURE__*/React.createElement("div", {
      style: {
        background: "rgba(201,95,95,0.08)",
        border: "1px solid rgba(201,95,95,0.25)",
        borderLeft: "3px solid #c95f5f",
        padding: "7px 10px",
        marginBottom: "10px",
        marginTop: "4px"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#c95f5f",
        fontSize: "8px",
        fontWeight: 700,
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        marginRight: "8px"
      }
    }, "\u26A0 WARNING"), /*#__PURE__*/React.createElement("span", {
      style: {
        color: "#e8b4b0",
        fontSize: "9.5px"
      }
    }, children));
  };
  var specTable = function specTable(headers, rows) {
    var colColors = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : [];
    return /*#__PURE__*/React.createElement("table", {
      style: {
        borderCollapse: "collapse",
        width: "100%",
        fontSize: "9.5px",
        marginTop: "8px",
        marginBottom: "4px"
      }
    }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
      style: {
        background: "#111410"
      }
    }, headers.map(function (h, i) {
      return /*#__PURE__*/React.createElement("th", {
        key: i,
        style: {
          padding: "5px 8px",
          textAlign: "left",
          color: colColors[i] || amber,
          fontSize: "7.5px",
          letterSpacing: "0.1em",
          textTransform: "uppercase",
          borderBottom: "1px solid ".concat(border),
          borderRight: i < headers.length - 1 ? "1px solid ".concat(border) : "none",
          fontWeight: 700
        }
      }, h);
    }))), /*#__PURE__*/React.createElement("tbody", null, rows.map(function (row, ri) {
      return /*#__PURE__*/React.createElement("tr", {
        key: ri,
        style: {
          background: ri % 2 === 0 ? "transparent" : "rgba(255,255,255,0.018)"
        }
      }, row.map(function (cell, ci) {
        return /*#__PURE__*/React.createElement("td", {
          key: ci,
          style: {
            padding: "5px 8px",
            color: ci === 0 ? white : ci === row.length - 1 && colColors[ci] === green ? green : textCol,
            fontSize: ci === 0 ? "10px" : "9.5px",
            fontWeight: ci === 0 ? "700" : "400",
            borderBottom: "1px solid #1a1c18",
            borderRight: ci < row.length - 1 ? "1px solid ".concat(border) : "none"
          }
        }, cell);
      }));
    })));
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: mono,
      fontSize: "10px",
      lineHeight: 1.6,
      color: textCol
    }
  }, /*#__PURE__*/React.createElement(DocHeader, null), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "12px 0 0 0"
    }
  }, /*#__PURE__*/React.createElement(Section, {
    num: "1.0",
    title: "Purpose & Scope"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "1.1"
  }, "This specification establishes the minimum requirements for the assembly, lubrication, torquing, and inspection of bolted flange connections on piping systems designed and constructed under ASME B31.3 ", /*#__PURE__*/React.createElement("em", null, "(Process Piping)"), " and ASME B31.8 ", /*#__PURE__*/React.createElement("em", null, "(Gas Transmission and Distribution Piping)"), " within Mustang Energy Partners, LLC facilities and projects."), /*#__PURE__*/React.createElement(Clause, {
    id: "1.2"
  }, "This specification applies to all ASME B16.5 flanged connections in Class 150 through Class 2500 service, including but not limited to: natural gas, condensate, produced water, sour service (H\u2082S partial pressure >0.0003 MPa), and hydrocarbon liquid service."), /*#__PURE__*/React.createElement(Clause, {
    id: "1.3"
  }, "Compliance with this specification is mandatory. Where conflicts exist between this document and referenced codes, the more stringent requirement shall govern. Conflicts shall be referred to the designated QC Authority for resolution prior to proceeding."), /*#__PURE__*/React.createElement(Clause, {
    id: "1.4",
    note: true
  }, "Note: This specification supplements, and does not replace, the requirements of ASME PCC-1 ", /*#__PURE__*/React.createElement("em", null, "Guidelines for Pressure Boundary Bolted Flange Joint Assembly"), ". Personnel performing flange assembly shall be familiar with the current edition of ASME PCC-1.")), /*#__PURE__*/React.createElement(Section, {
    num: "2.0",
    title: "Referenced Standards & Documents"
  }, specTable(["Document", "Title", "Edition / Note"], [["ASME B31.3", "Process Piping", "Current edition"], ["ASME B31.8", "Gas Transmission & Distribution Piping Systems", "Current edition"], ["ASME B16.5", "Pipe Flanges and Flanged Fittings NPS ½ through 24", "Current edition"], ["ASME B16.20", "Metallic Gaskets for Pipe Flanges", "Current edition"], ["ASME PCC-1", "Guidelines for Pressure Boundary Bolted Flange Joint Assembly", "Current edition"], ["ASTM A193", "Standard Specification for Alloy-Steel and SS Bolting for High-Temp or High-Pressure Service", "Grade B7 applies"], ["ASTM A194", "Standard Specification for Carbon and Alloy Steel Nuts for Bolts for High-Pressure or High-Temp Service", "Grade 2H applies"], ["NACE MR0175 / ISO 15156", "Petroleum and Natural Gas Industries — Materials for Use in H₂S-Containing Environments", "Sour service only"], ["MEP-QC-PROC-012", "Torque Wrench Calibration and Control Procedure", "Internal — mandatory"], ["MEP-QC-FORM-044A", "Flange Connection Torque Record", "Field documentation form"]])), /*#__PURE__*/React.createElement(Section, {
    num: "3.0",
    title: "Personnel Qualifications"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "3.1"
  }, "All personnel performing or supervising bolted flange assembly shall have completed MEP-approved flange assembly training within the preceding 36 months. Training records shall be available on request."), /*#__PURE__*/React.createElement(Clause, {
    id: "3.2"
  }, "QC Inspection of bolted flange assemblies shall be performed by a designated QC Inspector. The inspector shall record their full surname and first initial in ALL CAPS on form MEP-QC-FORM-044A (e.g., ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: amber
    }
  }, "J. SMITH"), "). Abbreviated or printed-name-only entries are not acceptable."), /*#__PURE__*/React.createElement(Clause, {
    id: "3.3"
  }, "Torque wrenches used in final assembly shall be calibrated per MEP-QC-PROC-012. The wrench identifier and calibration due date shall be recorded on form MEP-QC-FORM-044A prior to use. An expired calibration shall cause all torquing work performed with that wrench since its last valid calibration to be considered nonconforming.")), /*#__PURE__*/React.createElement(Section, {
    num: "4.0",
    title: "Material Requirements"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "4.1"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Bolting \u2014 General."), " Unless otherwise specified on the engineering drawing or piping material class, all stud bolts shall conform to ASTM A193 Grade B7 and all heavy hex nuts shall conform to ASTM A194 Grade 2H. No substitution of bolt or nut grade is permitted without written approval from the project Engineer of Record."), /*#__PURE__*/React.createElement(Clause, {
    id: "4.2"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Sour Service."), " For piping systems designated Sour Service (H\u2082S service per NACE MR0175 / ISO 15156), ASTM A193 B7 bolting is acceptable provided hardness does not exceed 35 HRC per heat. Mill Test Reports (MTRs) confirming hardness shall be on file prior to installation. Under no circumstances shall B7M or non-heat-treated material be substituted without EOR approval."), /*#__PURE__*/React.createElement(Clause, {
    id: "4.3"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Traceability."), " All bolts, nuts, and gaskets shall have documented traceability to a mill heat or lot certificate. The heat number (bolts/nuts) and lot number (gaskets) shall be recorded on MEP-QC-FORM-044A. Material installed without traceable certification is nonconforming and shall be removed."), /*#__PURE__*/React.createElement(Clause, {
    id: "4.4",
    note: true
  }, "Note: Mixed bolt grades (e.g., B7 and B8) within a single flange joint are strictly prohibited. All bolts in a joint shall be from the same specification and grade."), /*#__PURE__*/React.createElement(Warn, null, "Do not use galvanized or coated bolting in Class 600 or above service without explicit engineering approval. Hydrogen embrittlement risk is elevated in high-stress sour service applications.")), /*#__PURE__*/React.createElement(Section, {
    num: "5.0",
    title: "Gasket Requirements"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "5.1"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Type."), " For ASME B16.5 Class 150 through Class 2500 Raised Face (RF) connections in gas, sour gas, or hydrocarbon service, spiral wound gaskets (SWG) conforming to ASME B16.20 shall be used. SWGs shall be furnished with an outer centering ring and an inner retaining ring."), /*#__PURE__*/React.createElement(Clause, {
    id: "5.2"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Winding Material."), " For sour service or natural gas service at operating temperatures between -29\xB0C and 260\xB0C (-20\xB0F to 500\xB0F), the winding material shall be ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "316 Stainless Steel / Flexible Graphite"), " (316SS/FG). Ring material shall be carbon steel per ASME B16.20 unless otherwise specified."), /*#__PURE__*/React.createElement(Clause, {
    id: "5.3"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Lot Traceability."), " Each gasket lot shall be assigned a manufacturer's lot number. This lot number is a required entry on form MEP-QC-FORM-044A. The inspector shall verify the lot number from the gasket packaging label or certificate and record it verbatim. Do not estimate or interpolate lot numbers from adjacent joints."), /*#__PURE__*/React.createElement(Clause, {
    id: "5.4"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Inspection Prior to Installation."), " Each gasket shall be visually inspected prior to installation. Gaskets exhibiting crushed windings, separated layers, missing rings, scoring on seating surfaces, or corrosion shall be rejected and replaced. Rejected gaskets shall be marked and quarantined."), /*#__PURE__*/React.createElement(Clause, {
    id: "5.5"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Single Use Only."), " Spiral wound gaskets are single-use items. A gasket removed from a previously assembled joint shall not be reinstalled under any circumstances, regardless of apparent condition."), /*#__PURE__*/React.createElement(Clause, {
    id: "5.6",
    note: true
  }, "Note: Confirm gasket inner diameter (ID) does not restrict bore. The gasket ID shall be equal to or greater than the pipe bore. Oversized ID gaskets protruding into the flow stream are unacceptable and constitute a nonconformance.")), /*#__PURE__*/React.createElement(Section, {
    num: "6.0",
    title: "Flange Face Preparation"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "6.1"
  }, "Raised face surfaces shall be inspected for pitting, scoring, radial scratches, or mechanical damage prior to assembly. Defects exceeding 0.8 mm (1/32\") depth or crossing the gasket seating area are cause for rejection. Engineering disposition is required before proceeding."), /*#__PURE__*/React.createElement(Clause, {
    id: "6.2"
  }, "The required surface finish for raised face flanges in gas and sour service is ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "125 to 250 AARH (3.2 to 6.3 \xB5m Ra)"), ". Surface finish shall be verified by visual comparison to a reference coupon. Where doubt exists, profilometer measurement is required."), /*#__PURE__*/React.createElement(Clause, {
    id: "6.3"
  }, "Flange faces shall be clean and free of all foreign material, mill scale, paint, oils (other than assembly lubricant), and debris immediately prior to gasket installation. Cleaning shall be performed with a lint-free cloth and a solvent compatible with the service fluid."), /*#__PURE__*/React.createElement(Clause, {
    id: "6.4"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Alignment."), " Flanges shall be aligned so that the gap between flange faces is parallel (within 1/16\" per 12\" of pipe diameter) and the bolt holes are in alignment before any bolts are installed. \"Spring-loading\" a flange connection to achieve alignment is prohibited. Misalignment shall be corrected by spool adjustment, not by bolt load.")), /*#__PURE__*/React.createElement(Section, {
    num: "7.0",
    title: "Lubrication Requirements"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "7.1"
  }, "All bolt threads and bearing faces of nuts shall be lubricated prior to assembly. The approved lubricant for Class 600 and above in sour service applications is ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Molykote\xAE G-1000 PTFE-based thread paste"), " or an approved equal as listed on the MEP Qualified Products List (QPL)."), /*#__PURE__*/React.createElement(Clause, {
    id: "7.2"
  }, "Lubricant shall be applied to the full engaged thread length and to the underside of the nut bearing face. Excess lubricant shall not be applied such that it contacts the gasket seating face."), /*#__PURE__*/React.createElement(Clause, {
    id: "7.3"
  }, "The nut factor (K) for torque calculations in this specification is based on ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "K = 0.16"), ", applicable to lubricated ASTM A193 B7 / A194 2H assemblies. Dry or improperly lubricated assemblies will result in inadequate bolt load despite meeting the torque value \u2014 do not use the torque values in Table 1 without proper lubrication."), /*#__PURE__*/React.createElement(Clause, {
    id: "7.4",
    note: true
  }, "Note: The use of anti-seize compounds containing lead, zinc, or cadmium is prohibited on MEP facilities."), /*#__PURE__*/React.createElement(Warn, null, "Applying the torque values in Table 1 to dry (unlubricated) bolting will result in approximately 30\u201340% less actual bolt load than intended. This constitutes a latent joint integrity risk and is a nonconformance requiring disassembly and proper reassembly.")), /*#__PURE__*/React.createElement(Section, {
    num: "8.0",
    title: "Bolt Tightening Procedure"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "8.1"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "General."), " Bolt tightening shall be performed in accordance with ASME PCC-1 Appendix F (Recommended Bolt Tightening Sequence) using the cross (star) pattern as defined in clause 8.3 of this specification. No other tightening sequence is permitted without written approval from the QC Authority."), /*#__PURE__*/React.createElement(Clause, {
    id: "8.2"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Hand Tightening."), " Prior to torque application, all bolts shall be run down by hand until snug. Nuts shall turn freely by hand; any binding shall be investigated (misalignment, thread damage, or wrong bolt length) and corrected before proceeding."), /*#__PURE__*/React.createElement(Clause, {
    id: "8.3"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Cross (Star) Pattern."), " Number bolts sequentially clockwise from the 12 o'clock position (Bolt 1). Apply torque in the following cross sequence: begin at Bolt 1, proceed to the diametrically opposite bolt, then rotate approximately 90\xB0 clockwise and proceed to its opposite, continuing until all bolts have been torqued once. This completes one pass. Repeat for each subsequent pass."), /*#__PURE__*/React.createElement(Clause, {
    id: "8.4"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Multi-Pass Torquing."), " All joints shall be torqued in a minimum number of passes as specified in Table 1. Pass torque levels shall be as follows unless Table 1 specifies otherwise:"), specTable(["Pass", "% of Final Torque", "Purpose"], [["Pass 1 — Snug", "35% of Final", "Seat gasket, eliminate gap; cross pattern required"], ["Pass 2 — Intermediate", "70% of Final", "Distribute bolt load uniformly; cross pattern required"], ["Pass 3 — Final", "100% of Final", "Achieve target bolt load; cross pattern required"]]), /*#__PURE__*/React.createElement(TableNote, null, "For NPS 1.5\" and smaller in Class 600, a two-pass procedure is permitted: Pass 1 at 50% of final torque, Pass 2 at 100% of final torque, both in cross pattern."), /*#__PURE__*/React.createElement(Clause, {
    id: "8.5"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Achieved Torque."), " The achieved torque is the torque value recorded at the completion of the final pass on the final bolt in the sequence. If any bolt in the final pass is found to advance (move) upon application of the final torque value, the full cross-pattern final pass shall be repeated until no bolt advances. The highest stable torque value applied uniformly across all bolts constitutes the achieved torque."), /*#__PURE__*/React.createElement(Clause, {
    id: "8.6"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Over-Torquing."), " Torque values shall not exceed the maximum values specified in Table 1 footnotes. If a bolt breaks during torquing, the joint shall be disassembled, all bolts and nuts replaced, and the assembly restarted. Broken bolt stubs shall not be used."), /*#__PURE__*/React.createElement(Warn, null, "Do not use impact wrenches for final torque application. Calibrated torque wrenches (click-type or electronic) with a current calibration per MEP-QC-PROC-012 are required for all passes at and above 50% of final torque value.")), /*#__PURE__*/React.createElement(Section, {
    num: "9.0",
    title: "Torque Values \u2014 Table 1"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "9.1"
  }, "The following torque values apply to ASME B16.5 Raised Face flanged joints assembled per this specification using ASTM A193 B7 stud bolts, ASTM A194 2H heavy hex nuts, and Molykote\xAE G-1000 lubricant (K = 0.16). Values are in ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: amber
    }
  }, "ft-lb (foot-pounds)"), "."), specTable(["NPS", "Class", "Bolt Size", "No. Bolts", "Pass 1\nSnug (ft-lb)", "Pass 2\nInterm. (ft-lb)", "Final Torque\n(ft-lb)", "Min. Passes", "Max. Torque¹\n(ft-lb)"], [['½"', "600#", '½" × 3.25"', "4", "10", "20", "28", "3", "34"], ['¾"', "600#", '½" × 3.50"', "4", "12", "25", "35", "3", "42"], ['1"', "600#", '5/8" × 4.00"', "4", "18", "36", "50", "3", "60"], ['1½"', "600#", '5/8" × 4.50"', "8", "20", "—", "65", "2", "78"], ['2"', "600#", '¾" × 5.25"', "8", "28", "—", "75", "2", "90"], ['3"', "600#", '¾" × 5.75"', "12", "40", "80", "120", "3", "144"], ['4"', "600#", '7/8" × 6.25"', "16", "40", "80", "120", "3", "144"], ['6"', "600#", '1" × 7.25"', "16", "65", "130", "185", "3", "222"], ['8"', "600#", '1⅛" × 8.00"', "20", "90", "180", "270", "3", "324"], ['10"', "600#", '1¼" × 8.75"', "24", "120", "240", "360", "3", "432"], ['12"', "600#", '1¼" × 9.25"', "24", "130", "260", "390", "3", "468"]], [amber, muted, muted, muted, "#8ab4c4", "#8ab4c4", amber, white, muted]), /*#__PURE__*/React.createElement(TableNote, null, "\xB9 Maximum torque is 120% of final torque value. Bolts torqued beyond maximum shall be replaced prior to pressure testing. \u2014 Denotes not applicable (2-pass procedure); for 2-pass joints use 50% of Final for Pass 1."), /*#__PURE__*/React.createElement(TableNote, null, "This table applies to lubricated assemblies only (K=0.16). Do not apply these values to dry bolting. Class 150 and 300 torque values are in specification MEP-PIP-SPEC-044B.")), /*#__PURE__*/React.createElement(Section, {
    num: "10.0",
    title: "Inspection & Documentation"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "10.1"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Form MEP-QC-FORM-044A"), " (Flange Connection Torque Record) shall be completed for every bolted flange joint on systems covered by this specification. One form per joint. No joint shall be considered complete for hydrostatic test purposes until its form is signed, dated, and submitted to the project QC file."), /*#__PURE__*/React.createElement(Clause, {
    id: "10.2"
  }, "The QC Inspector shall verify and record the following on MEP-QC-FORM-044A for each joint: (a) joint identification number as shown on the isometric drawing; (b) line size and pressure class; (c) bolt size, material, and heat number; (d) nut material and heat number; (e) gasket type and lot number; (f) lubricant used; (g) torque wrench ID and calibration due date; (h) achieved torque value at final pass; (i) tightening pattern; (j) number of passes; (k) date, shift, and inspector initials."), /*#__PURE__*/React.createElement(Clause, {
    id: "10.3"
  }, /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Result Classification."), " A joint shall be classified ACC (Accepted) when: all above items are documented, achieved torque equals the final torque value from Table 1 \xB15%, no bolt was found not to advance during re-check, and no visible leakage or gasket extrusion is present. Any other condition shall be classified REJ (Rejected) pending Engineering disposition."), /*#__PURE__*/React.createElement(Clause, {
    id: "10.4"
  }, "The inspector shall record their identification as ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: amber
    }
  }, "INITIALS. SURNAME in all capital letters"), " (e.g., J. SMITH). This format is required for traceability to the individual's qualification record."), /*#__PURE__*/React.createElement(Clause, {
    id: "10.5",
    note: true
  }, "Note: Photocopied, pre-filled, or faxed forms are not acceptable as original quality records. Entries shall be made in permanent ink. Errors shall be crossed out with a single line, corrected, and initialed \u2014 not obliterated with correction fluid.")), /*#__PURE__*/React.createElement(Section, {
    num: "11.0",
    title: "Re-Torque Requirements"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "11.1"
  }, "All Class 600 and above joints in gas, sour gas, or hydrocarbon service shall be re-torqued within 24 hours of initial assembly or following the first thermal cycle above 65\xB0C (150\xB0F), whichever occurs first. Re-torquing shall use the same final torque value and cross pattern as initial assembly."), /*#__PURE__*/React.createElement(Clause, {
    id: "11.2"
  }, "If any bolt advances (moves) during re-torquing, the full cross-pattern final pass shall be completed until no bolt advances. The re-torque event and result shall be documented on MEP-QC-FORM-044A in the Remarks field."), /*#__PURE__*/React.createElement(Clause, {
    id: "11.3",
    note: true
  }, "Note: Re-torque is not required for Class 150 or 300 ambient-temperature non-cyclic service. Consult the QC Authority for non-standard service conditions.")), /*#__PURE__*/React.createElement(Section, {
    num: "12.0",
    title: "Nonconformance"
  }, /*#__PURE__*/React.createElement(Clause, {
    id: "12.1"
  }, "Any joint not meeting the requirements of this specification shall be identified as a Nonconformance (NCR) and shall not be hydrotested or placed in service until the NCR has been dispositioned by the Engineer of Record and QC Authority. Disposition options are: Use-As-Is (requires documented engineering justification), Rework, or Reject/Replace."), /*#__PURE__*/React.createElement(Clause, {
    id: "12.2"
  }, "Common nonconformances include, but are not limited to: missing MTR or gasket lot documentation; achieved torque outside \xB15% of final value; use of un-calibrated torque wrench; misalignment exceeding clause 6.4 tolerance; re-use of a spiral wound gasket; use of unapproved lubricant; and incomplete form MEP-QC-FORM-044A.")), /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: "1px solid ".concat(border),
      padding: "8px 10px",
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr",
      gap: "8px",
      background: "#080c07",
      marginTop: "8px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px"
    }
  }, "MEP-PIP-SPEC-044 Rev. 3", /*#__PURE__*/React.createElement("br", null), "Mustang Energy Partners, LLC"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      textAlign: "center"
    }
  }, "CONTROLLED DOCUMENT", /*#__PURE__*/React.createElement("br", null), "Printed copies are uncontrolled"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      textAlign: "right"
    }
  }, "Issued: 2024-11-15", /*#__PURE__*/React.createElement("br", null), "Next Review: 2026-11-15"))));
}

// ── REFERENCE PANEL ───────────────────────────────────────────
function RefPanel(_ref23) {
  var _ref23$hideJointForms = _ref23.hideJointForms,
    hideJointForms = _ref23$hideJointForms === void 0 ? false : _ref23$hideJointForms;
  var _useState11 = useState("drawing"),
    _useState12 = _slicedToArray(_useState11, 2),
    section = _useState12[0],
    setSection = _useState12[1];
  var _useState13 = useState("FLG-001"),
    _useState14 = _slicedToArray(_useState13, 2),
    activeJoint = _useState14[0],
    setActiveJoint = _useState14[1];
  var allSubTabs = [["drawing", "ISO Drawing"], ["forms", "Joint Forms"], ["torque", "Company Spec"], ["mtrs", "MTRs"], ["calcert", "Cal Cert"]];
  var subTabs = hideJointForms ? allSubTabs.filter(function (_ref24) {
    var _ref25 = _slicedToArray(_ref24, 1),
      id = _ref25[0];
    return id !== "forms";
  }) : allSubTabs;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      height: "100%",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      borderBottom: "1px solid ".concat(border),
      background: surf2,
      flexShrink: 0,
      flexWrap: "wrap"
    }
  }, subTabs.map(function (_ref26) {
    var _ref27 = _slicedToArray(_ref26, 2),
      id = _ref27[0],
      label = _ref27[1];
    return /*#__PURE__*/React.createElement("button", {
      key: id,
      onClick: function onClick() {
        return setSection(id);
      },
      style: {
        background: "none",
        border: "none",
        borderBottom: section === id ? "2px solid ".concat(amber) : "2px solid transparent",
        color: section === id ? amber : muted,
        cursor: "pointer",
        padding: "7px 12px",
        fontFamily: mono,
        fontSize: "8.5px",
        letterSpacing: "0.12em",
        textTransform: "uppercase"
      }
    }, label);
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "10px"
    }
  }, section === "drawing" && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      marginBottom: "6px"
    }
  }, SCENARIO.system, " \xB7 ASME B31.3 \xB7 P600 \xB7 Sour Service"), /*#__PURE__*/React.createElement("div", {
    style: {
      background: "#080d0a",
      border: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement(IsoMap, null))), section === "forms" && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "4px",
      marginBottom: "10px",
      flexWrap: "wrap"
    }
  }, SCENARIO.joints.map(function (j) {
    return /*#__PURE__*/React.createElement("button", {
      key: j.id,
      onClick: function onClick() {
        return setActiveJoint(j.id);
      },
      style: {
        background: activeJoint === j.id ? "rgba(212,131,42,0.15)" : "none",
        border: "1px solid ".concat(activeJoint === j.id ? amber : border),
        color: activeJoint === j.id ? amber : muted,
        cursor: "pointer",
        padding: "5px 10px",
        fontFamily: mono,
        fontSize: "8px",
        letterSpacing: "0.1em",
        textTransform: "uppercase"
      }
    }, j.id);
  })), /*#__PURE__*/React.createElement(JointForm, {
    f: JOINT_FORMS[activeJoint]
  })), section === "torque" && /*#__PURE__*/React.createElement(SpecDocument, null), section === "mtrs" && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      marginBottom: "8px"
    }
  }, "Mill Test Reports \xB7 ", SCENARIO.project), /*#__PURE__*/React.createElement(MTRPanel, null)), section === "calcert" && /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: muted,
      fontSize: "7.5px",
      letterSpacing: "0.1em",
      textTransform: "uppercase",
      marginBottom: "8px"
    }
  }, "Torque Wrench Calibration Certificate"), /*#__PURE__*/React.createElement(CalCertPanel, null))));
}

// ── MAIN APP ──────────────────────────────────────────────────
function TorqueLog() {
  var _useState15 = useState("brief"),
    _useState16 = _slicedToArray(_useState15, 2),
    tab = _useState16[0],
    setTab = _useState16[1];
  var _useState17 = useState(function () {
      return Object.fromEntries(SCENARIO.joints.map(function (j) {
        return [j.id, Object.fromEntries(COLS.map(function (c) {
          return [c.key, ""];
        }))];
      }));
    }),
    _useState18 = _slicedToArray(_useState17, 2),
    cells = _useState18[0],
    setCells = _useState18[1];
  var _useState19 = useState(false),
    _useState20 = _slicedToArray(_useState19, 2),
    submitted = _useState20[0],
    setSubmitted = _useState20[1];
  var _useState21 = useState(null),
    _useState22 = _slicedToArray(_useState21, 2),
    score = _useState22[0],
    setScore = _useState22[1];
  var _useState23 = useState(null),
    _useState24 = _slicedToArray(_useState23, 2),
    results = _useState24[0],
    setResults = _useState24[1];
  var _useState25 = useState(false),
    _useState26 = _slicedToArray(_useState25, 2),
    hints = _useState26[0],
    setHints = _useState26[1];
  var _useState27 = useState(null),
    _useState28 = _slicedToArray(_useState27, 2),
    activeCell = _useState28[0],
    setActiveCell = _useState28[1];
  var _useState29 = useState(1),
    _useState30 = _slicedToArray(_useState29, 2),
    workStep = _useState30[0],
    setWorkStep = _useState30[1];
  var _useState31 = useState(false),
    _useState32 = _slicedToArray(_useState31, 2),
    step1Complete = _useState32[0],
    setStep1Complete = _useState32[1];
  var inputRefs = useRef({});
  var update = function update(jid, key, val) {
    return setCells(function (p) {
      return _objectSpread(_objectSpread({}, p), {}, _defineProperty({}, jid, _objectSpread(_objectSpread({}, p[jid]), {}, _defineProperty({}, key, val))));
    });
  };
  var allFilled = SCENARIO.joints.every(function (j) {
    return COLS.every(function (c) {
      return cells[j.id][c.key].trim() !== "";
    });
  });
  var submit = function submit() {
    var tot = 0,
      cor = 0;
    var r = {};
    SCENARIO.joints.forEach(function (j) {
      r[j.id] = {};
      COLS.forEach(function (c) {
        tot++;
        var u = cells[j.id][c.key].trim().toUpperCase(),
          a = ANSWERS[j.id][c.key].toUpperCase(),
          ok = u === a;
        if (ok) cor++;
        r[j.id][c.key] = {
          ok: ok,
          u: u,
          a: a
        };
      });
    });
    setResults(r);
    setScore(Math.round(cor / tot * 100));
    setSubmitted(true);
  };
  var retry = function retry() {
    setCells(Object.fromEntries(SCENARIO.joints.map(function (j) {
      return [j.id, Object.fromEntries(COLS.map(function (c) {
        return [c.key, ""];
      }))];
    })));
    setSubmitted(false);
    setScore(null);
    setResults(null);
    setHints(false);
  };
  var passed = score !== null && score >= 80;
  var navToNext = function navToNext(ck) {
    var all = SCENARIO.joints.flatMap(function (j) {
      return COLS.map(function (c) {
        return "".concat(j.id, "|").concat(c.key);
      });
    });
    var next = all[all.indexOf(ck) + 1];
    if (next && inputRefs.current[next]) inputRefs.current[next].focus();
  };
  var Btn = function Btn(_ref28) {
    var children = _ref28.children,
      onClick = _ref28.onClick,
      _ref28$variant = _ref28.variant,
      variant = _ref28$variant === void 0 ? "primary" : _ref28$variant,
      _ref28$disabled = _ref28.disabled,
      disabled = _ref28$disabled === void 0 ? false : _ref28$disabled;
    var s = {
      primary: {
        background: amber,
        color: bg,
        border: "none"
      },
      ghost: {
        background: "none",
        color: muted,
        border: "1px solid ".concat(border)
      },
      success: {
        background: green,
        color: bg,
        border: "none"
      }
    };
    return /*#__PURE__*/React.createElement("button", {
      onClick: onClick,
      disabled: disabled,
      style: _objectSpread(_objectSpread({}, s[variant]), {}, {
        padding: "10px 20px",
        cursor: disabled ? "not-allowed" : "pointer",
        fontFamily: mono,
        fontSize: "11px",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        fontWeight: 600,
        opacity: disabled ? 0.4 : 1
      })
    }, children);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: mono,
      background: bg,
      color: textCol,
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      fontSize: "13px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: surf,
      borderBottom: "1px solid ".concat(border),
      padding: "10px 20px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "8px",
      letterSpacing: "0.2em",
      textTransform: "uppercase",
      marginBottom: "2px"
    }
  }, "FDQ Tier 2 \xB7 Practical Exercise"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: white,
      fontSize: "16px",
      fontWeight: 900,
      textTransform: "uppercase",
      letterSpacing: "0.06em"
    }
  }, "Bolted Flange Torque Log")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "16px"
    }
  }, submitted && /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "28px",
      fontWeight: 900,
      color: passed ? green : red,
      lineHeight: 1
    }
  }, score, "%"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "8px",
      color: passed ? green : red,
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, passed ? "✓ PASSED" : "✗ NOT PASSED")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      borderLeft: "1px solid ".concat(border),
      paddingLeft: "16px",
      gap: "4px"
    }
  }, [["brief", "Scenario"], ["work", "Work View"]].map(function (_ref29) {
    var _ref30 = _slicedToArray(_ref29, 2),
      id = _ref30[0],
      label = _ref30[1];
    return /*#__PURE__*/React.createElement("button", {
      key: id,
      onClick: function onClick() {
        return setTab(id);
      },
      style: {
        background: tab === id ? "rgba(212,131,42,0.12)" : "none",
        border: "1px solid ".concat(tab === id ? amber : border),
        color: tab === id ? amber : muted,
        cursor: "pointer",
        padding: "6px 14px",
        fontFamily: mono,
        fontSize: "9px",
        letterSpacing: "0.12em",
        textTransform: "uppercase"
      }
    }, label);
  })))), tab === "brief" && /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "20px",
      maxWidth: "860px",
      margin: "0 auto",
      width: "100%"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: surf,
      border: "1px solid ".concat(border),
      borderLeft: "3px solid ".concat(amber),
      padding: "18px 20px",
      marginBottom: "16px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: amber,
      fontSize: "9px",
      letterSpacing: "0.2em",
      textTransform: "uppercase",
      marginBottom: "10px"
    }
  }, "Exercise Brief"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "sans-serif",
      fontSize: "14px",
      lineHeight: 1.85,
      margin: 0
    }
  }, "You are the QC Inspector on ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Mustang Creek Compressor Station"), ". Bolted flange assembly for ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Discharge Piping \u2014 Train A"), " is complete. Switch to ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "Work View"), " to access the isometric drawing, individual joint torque forms, and Torque Specification \u2014 the Bill of Materials is embedded on the isometric drawing \u2014 all alongside the fillable log. Retrieve achieved torque values, gasket lot numbers, and all required data from the joint forms. Inspector: ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "J. Reed"), " \u2014 enter initials as ", /*#__PURE__*/React.createElement("strong", {
    style: {
      color: white
    }
  }, "J. REED"), ".")), /*#__PURE__*/React.createElement("div", {
    style: {
      background: surf,
      border: "1px solid ".concat(border),
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      marginBottom: "20px"
    }
  }, [["Project", SCENARIO.project], ["System", SCENARIO.system], ["Specification", SCENARIO.spec], ["Torque Procedure", SCENARIO.procedure], ["Fluid Service", SCENARIO.service], ["Gasket Lot #", SCENARIO.gasketLot], ["Inspector on Record", SCENARIO.inspector], ["Bolt Material", "ASTM A193 B7 / A194 2H"]].map(function (_ref31, i) {
    var _ref32 = _slicedToArray(_ref31, 2),
      l = _ref32[0],
      v = _ref32[1];
    return /*#__PURE__*/React.createElement("div", {
      key: l,
      style: {
        padding: "10px 14px",
        borderBottom: "1px solid ".concat(border),
        borderRight: i % 2 === 0 ? "1px solid ".concat(border) : "none",
        display: "flex",
        gap: "12px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: amber,
        fontSize: "8px",
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        width: "120px",
        flexShrink: 0
      }
    }, l), /*#__PURE__*/React.createElement("div", {
      style: {
        color: white,
        fontSize: "12px"
      }
    }, v));
  })), /*#__PURE__*/React.createElement(Btn, {
    onClick: function onClick() {
      return setTab("work");
    }
  }, "Open Work View \u2192")), tab === "work" && /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      background: surf2,
      borderBottom: "1px solid ".concat(border),
      flexShrink: 0,
      padding: "0 16px"
    }
  }, [["1", "Step 1 of 2 — Pre-Assembly Form", "Fill MEP-QC-FORM-044A from spec, MTRs & drawing"], ["2", "Step 2 of 2 — Torque Log", "Record achieved torque values after assembly"]].map(function (_ref33, i) {
    var _ref34 = _slicedToArray(_ref33, 3),
      num = _ref34[0],
      label = _ref34[1],
      desc = _ref34[2];
    return /*#__PURE__*/React.createElement("div", {
      key: num,
      onClick: function onClick() {
        if (num === "2" && step1Complete) setWorkStep(2);
        if (num === "1") setWorkStep(1);
      },
      style: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        padding: "8px 16px",
        cursor: num === "2" && !step1Complete ? "not-allowed" : "pointer",
        opacity: num === "2" && !step1Complete ? 0.35 : 1,
        borderBottom: workStep === parseInt(num) ? "2px solid ".concat(amber) : "2px solid transparent",
        marginBottom: "-1px"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: "18px",
        height: "18px",
        borderRadius: "50%",
        background: workStep === parseInt(num) ? "rgba(212,131,42,0.2)" : "transparent",
        border: "1px solid ".concat(workStep === parseInt(num) ? amber : border),
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: workStep === parseInt(num) ? amber : muted,
        fontSize: "8px",
        fontWeight: 700
      }
    }, num)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
      style: {
        color: workStep === parseInt(num) ? amber : muted,
        fontSize: "8.5px",
        fontWeight: 700,
        letterSpacing: "0.06em"
      }
    }, label), /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#3a3d37",
        fontSize: "7px",
        letterSpacing: "0.04em"
      }
    }, desc)), i === 0 && /*#__PURE__*/React.createElement("div", {
      style: {
        color: border,
        fontSize: "12px",
        marginLeft: "8px"
      }
    }, "\u203A"));
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: "52%",
      borderRight: "1px solid ".concat(border),
      display: "flex",
      flexDirection: "column",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "7px 12px",
      background: surf2,
      borderBottom: "1px solid ".concat(border),
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, workStep === 1 ? "MEP-QC-FORM-044A — FLG-001 · Suction Nozzle N1" : "Reference \xB7 ".concat(SCENARIO.system))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "12px"
    }
  }, workStep === 1 ? /*#__PURE__*/React.createElement(PreAssemblyForm, {
    onComplete: function onComplete() {
      setStep1Complete(true);
      setWorkStep(2);
    }
  }) : /*#__PURE__*/React.createElement(RefPanel, null))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      overflow: "hidden"
    }
  }, workStep === 1 ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "7px 12px",
      background: surf2,
      borderBottom: "1px solid ".concat(border),
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, "Reference \xB7 Spec / MTRs / Cal Cert / ISO Drawing")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement(RefPanel, {
    hideJointForms: true
  }))) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "7px 12px",
      background: surf2,
      borderBottom: "1px solid ".concat(border),
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.14em",
      textTransform: "uppercase"
    }
  }, "Torque Log \xB7 TQ-44A"), !submitted && /*#__PURE__*/React.createElement("button", {
    onClick: function onClick() {
      return setHints(function (h) {
        return !h;
      });
    },
    style: {
      background: "none",
      border: "1px solid ".concat(hints ? amber : border),
      color: hints ? amber : muted,
      padding: "3px 9px",
      cursor: "pointer",
      fontFamily: mono,
      fontSize: "8px",
      letterSpacing: "0.1em",
      textTransform: "uppercase"
    }
  }, hints ? "Hide Hints" : "Hints")), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: "auto",
      padding: "12px"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: surf,
      border: "1px solid ".concat(border),
      borderTop: "2px solid ".concat(amber),
      padding: "10px 12px",
      marginBottom: "10px",
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr",
      gap: "8px"
    }
  }, [["Project", SCENARIO.project], ["System", SCENARIO.system], ["Procedure", SCENARIO.procedure], ["Spec", SCENARIO.spec], ["Service", SCENARIO.service], ["Date", "___________"]].map(function (_ref35) {
    var _ref36 = _slicedToArray(_ref35, 2),
      l = _ref36[0],
      v = _ref36[1];
    return /*#__PURE__*/React.createElement("div", {
      key: l
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: amber,
        fontSize: "7px",
        letterSpacing: "0.14em",
        textTransform: "uppercase",
        marginBottom: "1px"
      }
    }, l), /*#__PURE__*/React.createElement("div", {
      style: {
        color: white,
        fontSize: "10px"
      }
    }, v));
  })), submitted && /*#__PURE__*/React.createElement("div", {
    style: {
      background: passed ? "rgba(82,163,102,0.12)" : "rgba(201,95,95,0.1)",
      border: "1px solid ".concat(passed ? "rgba(82,163,102,0.35)" : "rgba(201,95,95,0.3)"),
      padding: "9px 12px",
      marginBottom: "10px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: passed ? green : red,
      fontWeight: 700,
      fontSize: "12px"
    }
  }, passed ? "✓ PASSED" : "✗ NOT PASSED", " \u2014 ", score, "%", /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "10px",
      fontWeight: 400,
      marginLeft: "8px"
    }
  }, passed ? "Min. 80% required." : "Correct answers shown below cells.")), !passed && /*#__PURE__*/React.createElement("button", {
    onClick: retry,
    style: {
      background: "none",
      border: "1px solid ".concat(border),
      color: muted,
      padding: "5px 10px",
      cursor: "pointer",
      fontFamily: mono,
      fontSize: "9px",
      letterSpacing: "0.1em",
      textTransform: "uppercase"
    }
  }, "Retry")), /*#__PURE__*/React.createElement("div", {
    style: {
      overflowX: "auto",
      background: surf,
      border: "1px solid ".concat(border)
    }
  }, /*#__PURE__*/React.createElement("table", {
    style: {
      borderCollapse: "collapse",
      fontSize: "11px",
      width: "100%"
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", {
    style: {
      background: surf2
    }
  }, /*#__PURE__*/React.createElement("th", {
    style: {
      padding: "7px 8px",
      textAlign: "left",
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      borderBottom: "2px solid ".concat(border),
      borderRight: "1px solid ".concat(border),
      fontWeight: 500,
      whiteSpace: "nowrap"
    }
  }, "Joint"), /*#__PURE__*/React.createElement("th", {
    style: {
      padding: "7px 8px",
      textAlign: "left",
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      borderBottom: "2px solid ".concat(border),
      borderRight: "1px solid ".concat(border),
      fontWeight: 500,
      whiteSpace: "nowrap"
    }
  }, "Location"), /*#__PURE__*/React.createElement("th", {
    style: {
      padding: "7px 8px",
      textAlign: "left",
      color: muted,
      fontSize: "8px",
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      borderBottom: "2px solid ".concat(border),
      borderRight: "1px solid ".concat(border),
      fontWeight: 500,
      whiteSpace: "nowrap"
    }
  }, "Target"), COLS.map(function (col, ci) {
    return /*#__PURE__*/React.createElement("th", {
      key: col.key,
      style: {
        padding: "7px 8px",
        textAlign: "left",
        color: amber,
        fontSize: "8px",
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        borderBottom: "2px solid ".concat(amber),
        borderRight: ci < COLS.length - 1 ? "1px solid ".concat(border) : "none",
        fontWeight: 600,
        whiteSpace: "pre-line",
        minWidth: "72px"
      }
    }, col.label, hints && !submitted && /*#__PURE__*/React.createElement("div", {
      style: {
        color: "#3d3f39",
        fontSize: "7px",
        fontWeight: 400,
        marginTop: "1px"
      }
    }, col.hint));
  }))), /*#__PURE__*/React.createElement("tbody", null, SCENARIO.joints.map(function (j, ri) {
    return /*#__PURE__*/React.createElement("tr", {
      key: j.id,
      style: {
        borderBottom: "1px solid ".concat(border),
        background: ri % 2 === 0 ? "transparent" : "#1a1c18"
      }
    }, /*#__PURE__*/React.createElement("td", {
      style: {
        padding: "0 8px",
        height: "42px",
        color: amber,
        fontWeight: 600,
        borderRight: "1px solid ".concat(border),
        whiteSpace: "nowrap",
        fontSize: "11px"
      }
    }, j.id), /*#__PURE__*/React.createElement("td", {
      style: {
        padding: "0 8px",
        color: textCol,
        fontSize: "11px",
        borderRight: "1px solid ".concat(border),
        whiteSpace: "nowrap"
      }
    }, j.location), /*#__PURE__*/React.createElement("td", {
      style: {
        padding: "0 8px",
        color: white,
        fontWeight: 600,
        borderRight: "1px solid ".concat(border),
        whiteSpace: "nowrap"
      }
    }, j.target, " ft\xB7lb"), COLS.map(function (col, ci) {
      var _results$j$id;
      var ck = "".concat(j.id, "|").concat(col.key);
      var fr = submitted && (results === null || results === void 0 || (_results$j$id = results[j.id]) === null || _results$j$id === void 0 ? void 0 : _results$j$id[col.key]);
      var outlineColor = "transparent",
        cellBg = "transparent";
      if (activeCell === ck && !submitted) {
        outlineColor = amber;
        cellBg = "rgba(212,131,42,0.08)";
      }
      if (submitted) {
        cellBg = fr !== null && fr !== void 0 && fr.ok ? "rgba(82,163,102,0.1)" : "rgba(201,95,95,0.08)";
        outlineColor = fr !== null && fr !== void 0 && fr.ok ? "rgba(82,163,102,0.4)" : "rgba(201,95,95,0.4)";
      }
      return /*#__PURE__*/React.createElement("td", {
        key: col.key,
        style: {
          padding: 0,
          borderRight: ci < COLS.length - 1 ? "1px solid ".concat(border) : "none"
        }
      }, /*#__PURE__*/React.createElement("div", {
        style: {
          outline: "2px solid ".concat(outlineColor),
          outlineOffset: "-2px",
          background: cellBg,
          minHeight: "42px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center"
        }
      }, /*#__PURE__*/React.createElement("input", {
        ref: function ref(el) {
          if (el) inputRefs.current[ck] = el;
        },
        value: cells[j.id][col.key],
        disabled: submitted,
        onChange: function onChange(e) {
          return update(j.id, col.key, e.target.value);
        },
        onFocus: function onFocus() {
          return setActiveCell(ck);
        },
        onBlur: function onBlur() {
          return setActiveCell(null);
        },
        onKeyDown: function onKeyDown(e) {
          if (e.key === "Tab" || e.key === "Enter") {
            e.preventDefault();
            navToNext(ck);
          }
        },
        placeholder: hints && !submitted ? col.hint : "",
        style: {
          width: "100%",
          background: "transparent",
          border: "none",
          outline: "none",
          color: submitted ? fr !== null && fr !== void 0 && fr.ok ? green : red : white,
          padding: "8px",
          fontSize: "11px",
          fontFamily: mono,
          cursor: submitted ? "default" : "text",
          boxSizing: "border-box"
        }
      }), submitted && fr && !fr.ok && /*#__PURE__*/React.createElement("div", {
        style: {
          padding: "0 8px 5px",
          fontSize: "8px",
          color: green,
          letterSpacing: "0.06em"
        }
      }, "\u2713 ", fr.a)));
    }));
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      color: "#3d3f39",
      fontSize: "8px",
      marginTop: "5px",
      letterSpacing: "0.1em"
    }
  }, "TAB or ENTER to advance"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "14px",
      display: "flex",
      justifyContent: "flex-end",
      gap: "10px",
      alignItems: "center"
    }
  }, !submitted && !allFilled && /*#__PURE__*/React.createElement("span", {
    style: {
      color: muted,
      fontSize: "9px"
    }
  }, "Fill all cells to submit"), !submitted && /*#__PURE__*/React.createElement(Btn, {
    onClick: submit,
    disabled: !allFilled
  }, "Submit Log"), submitted && passed && /*#__PURE__*/React.createElement(Btn, {
    variant: "success",
    onClick: function onClick() {
      if (!window.SUBMIT_URL) return;
      fetch(window.SUBMIT_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.CSRF_TOKEN || '',
        },
        body: JSON.stringify({
          step: 2,
          score: score,
          passed: true,
          response_data: {}
        })
      })
      .then(function(r) { return r.json(); })
      .then(function() {
        var tierSlug = window.TIER_SLUG || 'practitioner';
        window.location.href = '/certifications/' + tierSlug + '/learn/';
      })
      .catch(function() {
        var tierSlug = window.TIER_SLUG || 'practitioner';
        window.location.href = '/certifications/' + tierSlug + '/learn/';
      });
    }
  }, "Exercise Complete \u2713"))))))));
}

// ── WELD INSPECTION LOG ──────────────────────────────────────
function WeldLog() {
  var CFG = window.EXERCISE_CONFIG || {};
  var steps = CFG.steps || [];
  var welds = (CFG.scenario && CFG.scenario.welds) || [];
  var wpss = (CFG.scenario && CFG.scenario.wpss) || [];
  var welders = (CFG.scenario && CFG.scenario.welders) || [];
  var pipeMtrs = (CFG.scenario && CFG.scenario.pipe_mtrs) || [];
  var fillerCerts = (CFG.scenario && CFG.scenario.filler_certs) || [];
  var travelers = (CFG.scenario && CFG.scenario.travelers) || [];
  var stepFields = CFG.step_fields || {};
  var answers = CFG.answers || {};

  // ── State ────────────────────────────────────────────────────
  var _s1 = useState("brief"),
    _s1a = _slicedToArray(_s1, 2),
    tab = _s1a[0],
    setTab = _s1a[1];

  var _s2 = useState(steps.length > 0 ? steps[0].id : "step_1"),
    _s2a = _slicedToArray(_s2, 2),
    activeStep = _s2a[0],
    setActiveStep = _s2a[1];

  var _s3 = useState(function () {
      var d = {};
      steps.forEach(function (st) {
        d[st.id] = {};
        if (st.scope === "single") {
          d[st.id]["WLD-001"] = {};
          var fields = stepFields[st.id] || [];
          fields.forEach(function (f) { d[st.id]["WLD-001"][f.key] = ""; });
        } else {
          var pipeExtra = [
            { key: "pipe_grade" }, { key: "pipe_od" }, { key: "pipe_wt" }
          ];
          welds.forEach(function (w) {
            d[st.id][w.id] = {};
            var fields = pipeExtra.concat(stepFields[st.id] || []);
            fields.forEach(function (f) { d[st.id][w.id][f.key] = ""; });
          });
        }
      });
      return d;
    }),
    _s3a = _slicedToArray(_s3, 2),
    formData = _s3a[0],
    setFormData = _s3a[1];

  var _s4 = useState({}),
    _s4a = _slicedToArray(_s4, 2),
    submitted = _s4a[0],
    setSubmitted = _s4a[1];

  var _s5 = useState({}),
    _s5a = _slicedToArray(_s5, 2),
    scores = _s5a[0],
    setScores = _s5a[1];

  var _s6 = useState({}),
    _s6a = _slicedToArray(_s6, 2),
    stepScores = _s6a[0],
    setStepScores = _s6a[1];

  var _s7 = useState({}),
    _s7a = _slicedToArray(_s7, 2),
    stepPassed = _s7a[0],
    setStepPassed = _s7a[1];

  var _s8 = useState(null),
    _s8a = _slicedToArray(_s8, 2),
    activeCell = _s8a[0],
    setActiveCell = _s8a[1];

  var _s9 = useState("weldmap"),
    _s9a = _slicedToArray(_s9, 2),
    refTab = _s9a[0],
    setRefTab = _s9a[1];

  var _s10 = useState(wpss.length > 0 ? wpss[0].id || "wps_0" : "wps_0"),
    _s10a = _slicedToArray(_s10, 2),
    activeWps = _s10a[0],
    setActiveWps = _s10a[1];

  var _s11 = useState(welders.length > 0 ? welders[0].id || "welder_0" : "welder_0"),
    _s11a = _slicedToArray(_s11, 2),
    activeWelder = _s11a[0],
    setActiveWelder = _s11a[1];

  var _s12 = useState(travelers.length > 0 ? travelers[0].weld_id || "WLD-001" : "WLD-001"),
    _s12a = _slicedToArray(_s12, 2),
    activeTraveler = _s12a[0],
    setActiveTraveler = _s12a[1];

  var _s13 = useState(pipeMtrs.length > 0 ? pipeMtrs[0].id || "mtr_0" : "mtr_0"),
    _s13a = _slicedToArray(_s13, 2),
    activePipeMtr = _s13a[0],
    setActivePipeMtr = _s13a[1];

  var _s14 = useState(fillerCerts.length > 0 ? fillerCerts[0].id || "fc_0" : "fc_0"),
    _s14a = _slicedToArray(_s14, 2),
    activeFillerCert = _s14a[0],
    setActiveFillerCert = _s14a[1];

  var _s15 = useState(false),
    _s15a = _slicedToArray(_s15, 2),
    exerciseDone = _s15a[0],
    setExerciseDone = _s15a[1];

  var inputRefs = useRef({});

  // ── Helpers ──────────────────────────────────────────────────
  var updateField = function (stepId, weldId, key, val) {
    setFormData(function (prev) {
      var copy = _objectSpread({}, prev);
      copy[stepId] = _objectSpread({}, copy[stepId]);
      copy[stepId][weldId] = _objectSpread({}, copy[stepId][weldId]);
      copy[stepId][weldId][key] = val;
      return copy;
    });
  };

  var getStep = function (id) {
    return steps.find(function (s) { return s.id === id; }) || {};
  };

  var stepIndex = function (id) {
    for (var i = 0; i < steps.length; i++) {
      if (steps[i].id === id) return i;
    }
    return 0;
  };

  var isStepUnlocked = function (id) {
    var idx = stepIndex(id);
    if (idx === 0) return true;
    var prev = steps[idx - 1];
    return !!stepPassed[prev.id];
  };

  var currentStep = getStep(activeStep);
  var currentFields = getFieldsForStep(activeStep);
  var currentAnswers = answers[activeStep] || {};

  // Group fields by section for single-weld steps
  var fieldSections = [];
  if (currentStep.scope === "single") {
    var sMap = {};
    var sOrder = [];
    currentFields.forEach(function (f) {
      var sec = f.section || "general";
      if (!sMap[sec]) {
        sMap[sec] = [];
        sOrder.push(sec);
      }
      sMap[sec].push(f);
    });
    sOrder.forEach(function (sec) {
      fieldSections.push({ id: sec, label: sec.replace(/_/g, " "), fields: sMap[sec] });
    });
  }

  // ── Scoring ──────────────────────────────────────────────────
  var pipeExtraColsDef = [
    { key: "pipe_grade", label: "Pipe\nGrade", hint: "e.g. API 5L X65" },
    { key: "pipe_od", label: "Pipe\nOD", hint: 'e.g. 12.750"' },
    { key: "pipe_wt", label: "Wall\nThickness", hint: 'e.g. 0.375"' }
  ];

  var getFieldsForStep = function (stepId) {
    var fields = stepFields[stepId] || [];
    if (stepId === "wps_verification") {
      return fields.filter(function (f) {
        return f.key !== "positions_covered" && f.key !== "od_range" && f.key !== "wall_range";
      });
    }
    var st = getStep(stepId);
    if (st.scope === "table") {
      return pipeExtraColsDef.concat(fields);
    }
    return fields;
  };

  var allFilledForStep = function (stepId) {
    var st = getStep(stepId);
    var fields = getFieldsForStep(stepId);
    if (st.scope === "single") {
      return fields.every(function (f) {
        return formData[stepId] && formData[stepId]["WLD-001"] && formData[stepId]["WLD-001"][f.key] && formData[stepId]["WLD-001"][f.key].trim() !== "";
      });
    } else {
      return welds.every(function (w) {
        return fields.every(function (f) {
          return formData[stepId] && formData[stepId][w.id] && formData[stepId][w.id][f.key] && formData[stepId][w.id][f.key].trim() !== "";
        });
      });
    }
  };

  var handleSubmitStep = function (stepId) {
    var st = getStep(stepId);
    var fields = getFieldsForStep(stepId);
    var ans = answers[stepId] || {};
    var totalCor = 0, totalFields = 0;
    var sc = {};

    if (st.scope === "single") {
      var wId = "WLD-001";
      sc[wId] = {};
      var wAns = ans[wId] || ans;
      fields.forEach(function (f) {
        totalFields++;
        var userVal = (formData[stepId][wId][f.key] || "").trim();
        var correctVal = (wAns[f.key] || "").toString();
        var ok = checkFormField(f.key, userVal, correctVal);
        if (ok) totalCor++;
        sc[wId][f.key] = { ok: ok, entered: userVal, correct: correctVal };
      });
    } else {
      var pipeAnswerMap = { pipe_grade: "pipe_spec", pipe_od: "od", pipe_wt: "wt" };
      welds.forEach(function (w) {
        sc[w.id] = {};
        var wAns = ans[w.id] || {};
        fields.forEach(function (f) {
          totalFields++;
          var userVal = (formData[stepId][w.id][f.key] || "").trim();
          var correctVal;
          if (pipeAnswerMap[f.key]) {
            correctVal = (w[pipeAnswerMap[f.key]] || "").toString();
          } else {
            correctVal = (wAns[f.key] || "").toString();
          }
          var ok = checkFormField(f.key, userVal, correctVal);
          if (ok) totalCor++;
          sc[w.id][f.key] = { ok: ok, entered: userVal, correct: correctVal };
        });
      });
    }

    var pct = totalFields > 0 ? Math.round(totalCor / totalFields * 100) : 0;
    var pass = pct >= 80;

    setScores(function (prev) {
      return _objectSpread(_objectSpread({}, prev), _defineProperty({}, stepId, sc));
    });
    setStepScores(function (prev) {
      return _objectSpread(_objectSpread({}, prev), _defineProperty({}, stepId, pct));
    });
    setSubmitted(function (prev) {
      return _objectSpread(_objectSpread({}, prev), _defineProperty({}, stepId, true));
    });
    setStepPassed(function (prev) {
      return _objectSpread(_objectSpread({}, prev), _defineProperty({}, stepId, pass));
    });
  };

  var handleRetry = function (stepId) {
    var st = getStep(stepId);
    var fields = stepFields[stepId] || [];
    setFormData(function (prev) {
      var copy = _objectSpread({}, prev);
      copy[stepId] = {};
      if (st.scope === "single") {
        copy[stepId]["WLD-001"] = {};
        fields.forEach(function (f) { copy[stepId]["WLD-001"][f.key] = ""; });
      } else {
        welds.forEach(function (w) {
          copy[stepId][w.id] = {};
          fields.forEach(function (f) { copy[stepId][w.id][f.key] = ""; });
        });
      }
      return copy;
    });
    setSubmitted(function (prev) {
      var c = _objectSpread({}, prev);
      delete c[stepId];
      return c;
    });
    setScores(function (prev) {
      var c = _objectSpread({}, prev);
      delete c[stepId];
      return c;
    });
    setStepScores(function (prev) {
      var c = _objectSpread({}, prev);
      delete c[stepId];
      return c;
    });
    setStepPassed(function (prev) {
      var c = _objectSpread({}, prev);
      delete c[stepId];
      return c;
    });
  };

  // Tab navigation for table steps
  var navToNext = function (stepId, ck) {
    var fields = stepFields[stepId] || [];
    var all = welds.flatMap(function (w) {
      return fields.map(function (f) {
        return w.id + "|" + f.key;
      });
    });
    var idx = all.indexOf(ck);
    var next = all[idx + 1];
    if (next && inputRefs.current[stepId + "|" + next]) {
      inputRefs.current[stepId + "|" + next].focus();
    }
  };

  // Exercise complete handler
  var handleExerciseComplete = function () {
    if (!window.SUBMIT_URL) return;
    setExerciseDone(true);
    var lastStep = steps[steps.length - 1];
    fetch(window.SUBMIT_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.CSRF_TOKEN || ""
      },
      body: JSON.stringify({
        step: steps.length,
        score: stepScores[lastStep.id],
        passed: true,
        response_data: {}
      })
    })
    .then(function (r) { return r.json(); })
    .then(function () {
      var tierSlug = window.TIER_SLUG || "practitioner";
      window.location.href = "/certifications/" + tierSlug + "/learn/";
    })
    .catch(function () {
      var tierSlug = window.TIER_SLUG || "practitioner";
      window.location.href = "/certifications/" + tierSlug + "/learn/";
    });
  };

  // ── Button helper ────────────────────────────────────────────
  var Btn = function (props) {
    var variant = props.variant || "primary";
    var s = {
      primary: { background: amber, color: bg, border: "none" },
      ghost: { background: "none", color: muted, border: "1px solid " + border },
      success: { background: green, color: bg, border: "none" }
    };
    return React.createElement("button", {
      onClick: props.onClick,
      disabled: props.disabled || false,
      style: _objectSpread(_objectSpread({}, s[variant] || s.primary), {
        padding: "10px 20px",
        cursor: props.disabled ? "not-allowed" : "pointer",
        fontFamily: mono,
        fontSize: "11px",
        letterSpacing: "0.12em",
        textTransform: "uppercase",
        fontWeight: 600,
        opacity: props.disabled ? 0.4 : 1
      })
    }, props.children);
  };

  // ── Weld Map SVG ─────────────────────────────────────────────
  var renderWeldMap = function () {
    var weldPositions = [
      { x: 200, y: 80, label: welds[0] ? welds[0].id : "WLD-001" },
      { x: 620, y: 80, label: welds[1] ? welds[1].id : "WLD-002" },
      { x: 120, y: 280, label: welds[2] ? welds[2].id : "WLD-003" },
      { x: 460, y: 320, label: welds[3] ? welds[3].id : "WLD-004" },
      { x: 700, y: 280, label: welds[4] ? welds[4].id : "WLD-005" }
    ];
    return React.createElement("svg", {
      viewBox: "0 0 860 440",
      width: "100%",
      style: { display: "block", fontFamily: "IBM Plex Mono, monospace" }
    },
      // Background
      React.createElement("rect", { width: "860", height: "440", fill: "#0a0b09" }),
      // Grid
      React.createElement("g", { stroke: "#1e211a", strokeWidth: "0.5", strokeDasharray: "3,9" },
        React.createElement("line", { x1: "0", y1: "110", x2: "860", y2: "110" }),
        React.createElement("line", { x1: "0", y1: "220", x2: "860", y2: "220" }),
        React.createElement("line", { x1: "0", y1: "330", x2: "860", y2: "330" }),
        React.createElement("line", { x1: "215", y1: "0", x2: "215", y2: "440" }),
        React.createElement("line", { x1: "430", y1: "0", x2: "430", y2: "440" }),
        React.createElement("line", { x1: "645", y1: "0", x2: "645", y2: "440" })
      ),
      // Compressor box
      React.createElement("rect", { x: "350", y: "160", width: "160", height: "100", fill: "#0f1812", stroke: "#1e3828", strokeWidth: "1.5", rx: "3" }),
      React.createElement("line", { x1: "350", y1: "190", x2: "510", y2: "190", stroke: "#1c3024", strokeWidth: "0.8", strokeDasharray: "4,4" }),
      React.createElement("line", { x1: "350", y1: "230", x2: "510", y2: "230", stroke: "#1c3024", strokeWidth: "0.8", strokeDasharray: "4,4" }),
      React.createElement("text", { x: "395", y: "215", fill: "#2d5240", fontSize: "10", fontWeight: "700", letterSpacing: "0.1em" }, "COMP-A"),
      React.createElement("text", { x: "400", y: "227", fill: "#233d30", fontSize: "8" }, "TRAIN A"),
      // Pipe runs
      React.createElement("line", { x1: "80", y1: "120", x2: "350", y2: "120", stroke: steel, strokeWidth: "4" }),
      React.createElement("line", { x1: "510", y1: "120", x2: "780", y2: "120", stroke: steel, strokeWidth: "4" }),
      React.createElement("line", { x1: "80", y1: "320", x2: "350", y2: "320", stroke: steel, strokeWidth: "4" }),
      React.createElement("line", { x1: "510", y1: "320", x2: "780", y2: "320", stroke: steel, strokeWidth: "4" }),
      React.createElement("line", { x1: "350", y1: "210", x2: "80", y2: "210", stroke: steel, strokeWidth: "3", strokeDasharray: "8,4" }),
      // Weld callout boxes
      weldPositions.map(function (wp, i) {
        var w = welds[i];
        var desc = w ? (w.size || "") + " " + (w.type || "") : "";
        return React.createElement("g", { key: wp.label },
          // Leader line
          React.createElement("line", {
            x1: wp.x + 40, y1: wp.y + 40,
            x2: wp.x + 40, y2: wp.y < 200 ? wp.y + 60 : wp.y - 10,
            stroke: "#3a556a", strokeWidth: "0.8", strokeDasharray: "2,3"
          }),
          // Diamond symbol
          React.createElement("polygon", {
            points: (wp.x + 40) + "," + (wp.y < 200 ? wp.y + 60 : wp.y - 10) + " " + (wp.x + 44) + "," + (wp.y < 200 ? wp.y + 66 : wp.y - 16) + " " + (wp.x + 40) + "," + (wp.y < 200 ? wp.y + 72 : wp.y - 22) + " " + (wp.x + 36) + "," + (wp.y < 200 ? wp.y + 66 : wp.y - 16),
            fill: "none", stroke: amber, strokeWidth: "1"
          }),
          // Callout box
          React.createElement("rect", {
            x: wp.x, y: wp.y, width: 80, height: 38,
            fill: "rgba(22,23,20,0.95)", stroke: amber, strokeWidth: "1", rx: "2"
          }),
          React.createElement("text", {
            x: wp.x + 40, y: wp.y + 15,
            fill: amber, fontSize: "9", fontWeight: "700", textAnchor: "middle", letterSpacing: "0.08em"
          }, wp.label),
          React.createElement("text", {
            x: wp.x + 40, y: wp.y + 28,
            fill: muted, fontSize: "7", textAnchor: "middle"
          }, desc)
        );
      }),
      // Title block
      React.createElement("rect", { x: "580", y: "370", width: "260", height: "55", fill: "#111410", stroke: "#1e211a", strokeWidth: "1" }),
      React.createElement("text", { x: "595", y: "388", fill: muted, fontSize: "7", letterSpacing: "0.1em" }, "WELD MAP"),
      React.createElement("text", { x: "595", y: "400", fill: white, fontSize: "9", fontWeight: "700" }, CFG.scenario ? CFG.scenario.project || "" : ""),
      React.createElement("text", { x: "595", y: "412", fill: muted, fontSize: "7" }, CFG.scenario ? CFG.scenario.system || "" : ""),
      React.createElement("text", { x: "595", y: "422", fill: "#2d5240", fontSize: "6.5" }, welds.length + " WELDS IDENTIFIED")
    );
  };

  // ── Reference Panel: WPS Docs ──────────────────────────────
  var renderWpsDocs = function () {
    var wps = wpss.find(function (w) { return (w.id || w.wps_no) === activeWps; }) || wpss[0] || {};
    var wpsFields = [];
    Object.keys(wps).forEach(function (k) {
      if (k !== "id" && k !== "chemistry" && k !== "mechanical") {
        wpsFields.push([k.replace(/_/g, " "), wps[k]]);
      }
    });
    return React.createElement("div", null,
      React.createElement("div", { style: { display: "flex", gap: "4px", marginBottom: "10px", flexWrap: "wrap" } },
        wpss.map(function (w) {
          var wid = w.id || w.wps_no || "wps";
          return React.createElement("button", {
            key: wid,
            onClick: function () { setActiveWps(wid); },
            style: {
              background: activeWps === wid ? "rgba(212,131,42,0.15)" : "none",
              border: "1px solid " + (activeWps === wid ? amber : border),
              color: activeWps === wid ? amber : muted,
              cursor: "pointer", padding: "5px 10px", fontFamily: mono,
              fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase"
            }
          }, w.wps_no || wid);
        })
      ),
      React.createElement("div", { style: { background: surf, border: "1px solid " + border } },
        wpsFields.map(function (pair, i) {
          return React.createElement("div", {
            key: i,
            style: {
              display: "grid", gridTemplateColumns: "160px 1fr",
              borderBottom: i < wpsFields.length - 1 ? "1px solid " + border : "none"
            }
          },
            React.createElement("div", {
              style: { padding: "5px 10px", background: surf2, borderRight: "1px solid " + border, color: muted, fontSize: "8px", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600 }
            }, pair[0]),
            React.createElement("div", {
              style: { padding: "5px 10px", color: white, fontSize: "10px" }
            }, typeof pair[1] === "object" ? JSON.stringify(pair[1]) : String(pair[1] || ""))
          );
        })
      )
    );
  };

  // ── Reference Panel: WQRs ──────────────────────────────────
  var renderWqrs = function () {
    var welder = welders.find(function (w) { return (w.id || w.stamp) === activeWelder; }) || welders[0] || {};
    var welderFields = [];
    Object.keys(welder).forEach(function (k) {
      if (k !== "id") {
        welderFields.push([k.replace(/_/g, " "), welder[k]]);
      }
    });
    return React.createElement("div", null,
      React.createElement("div", { style: { display: "flex", gap: "4px", marginBottom: "10px", flexWrap: "wrap" } },
        welders.map(function (w) {
          var wid = w.id || w.stamp || "welder";
          return React.createElement("button", {
            key: wid,
            onClick: function () { setActiveWelder(wid); },
            style: {
              background: activeWelder === wid ? "rgba(212,131,42,0.15)" : "none",
              border: "1px solid " + (activeWelder === wid ? amber : border),
              color: activeWelder === wid ? amber : muted,
              cursor: "pointer", padding: "5px 10px", fontFamily: mono,
              fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase"
            }
          }, w.name || w.stamp || wid);
        })
      ),
      React.createElement("div", { style: { background: surf, border: "1px solid " + border } },
        welderFields.map(function (pair, i) {
          return React.createElement("div", {
            key: i,
            style: {
              display: "grid", gridTemplateColumns: "160px 1fr",
              borderBottom: i < welderFields.length - 1 ? "1px solid " + border : "none"
            }
          },
            React.createElement("div", {
              style: { padding: "5px 10px", background: surf2, borderRight: "1px solid " + border, color: muted, fontSize: "8px", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600 }
            }, pair[0]),
            React.createElement("div", {
              style: { padding: "5px 10px", color: white, fontSize: "10px" }
            }, Array.isArray(pair[1]) ? pair[1].join(", ") : (typeof pair[1] === "object" ? JSON.stringify(pair[1]) : String(pair[1] || "")))
          );
        })
      )
    );
  };

  // ── Reference Panel: Travelers ─────────────────────────────
  var renderTravelers = function () {
    var trav = travelers.find(function (t) { return (t.weld_id || t.id) === activeTraveler; }) || travelers[0] || {};
    var travFields = [];
    Object.keys(trav).forEach(function (k) {
      if (k !== "pass_log" && k !== "id") {
        travFields.push([k.replace(/_/g, " "), trav[k]]);
      }
    });
    var passLog = trav.pass_log || [];
    return React.createElement("div", null,
      React.createElement("div", { style: { display: "flex", gap: "4px", marginBottom: "10px", flexWrap: "wrap" } },
        travelers.map(function (t) {
          var tid = t.weld_id || t.id || "trav";
          return React.createElement("button", {
            key: tid,
            onClick: function () { setActiveTraveler(tid); },
            style: {
              background: activeTraveler === tid ? "rgba(212,131,42,0.15)" : "none",
              border: "1px solid " + (activeTraveler === tid ? amber : border),
              color: activeTraveler === tid ? amber : muted,
              cursor: "pointer", padding: "5px 10px", fontFamily: mono,
              fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase"
            }
          }, tid);
        })
      ),
      // Traveler fields
      React.createElement("div", { style: { background: surf, border: "1px solid " + border, marginBottom: "10px" } },
        travFields.map(function (pair, i) {
          return React.createElement("div", {
            key: i,
            style: {
              display: "grid", gridTemplateColumns: "160px 1fr",
              borderBottom: i < travFields.length - 1 ? "1px solid " + border : "none"
            }
          },
            React.createElement("div", {
              style: { padding: "5px 10px", background: surf2, borderRight: "1px solid " + border, color: muted, fontSize: "8px", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600 }
            }, pair[0]),
            React.createElement("div", {
              style: { padding: "5px 10px", color: white, fontSize: "10px" }
            }, typeof pair[1] === "object" ? JSON.stringify(pair[1]) : String(pair[1] || ""))
          );
        })
      ),
      // Pass log table
      passLog.length > 0 ? React.createElement("div", null,
        React.createElement("div", { style: { color: amber, fontSize: "8px", letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: "6px" } }, "Pass Log"),
        React.createElement("table", { style: { borderCollapse: "collapse", width: "100%", fontSize: "8.5px" } },
          React.createElement("thead", null,
            React.createElement("tr", { style: { background: "#111410" } },
              Object.keys(passLog[0]).map(function (hk) {
                return React.createElement("th", {
                  key: hk,
                  style: { padding: "5px 6px", textAlign: "left", color: amber, fontSize: "7.5px", letterSpacing: "0.08em", textTransform: "uppercase", borderBottom: "1px solid " + border, borderRight: "1px solid " + border, fontWeight: 600 }
                }, hk.replace(/_/g, " "));
              })
            )
          ),
          React.createElement("tbody", null,
            passLog.map(function (row, ri) {
              return React.createElement("tr", { key: ri, style: { borderBottom: "1px solid " + border, background: ri % 2 === 0 ? "transparent" : "#1a1c18" } },
                Object.keys(row).map(function (ck, ci) {
                  return React.createElement("td", {
                    key: ci,
                    style: { padding: "4px 6px", color: textCol, fontSize: "9px", borderRight: "1px solid " + border }
                  }, String(row[ck] || ""));
                })
              );
            })
          )
        )
      ) : null
    );
  };

  // ── Reference Panel: Pipe MTRs ─────────────────────────────
  var renderMtrPanel = function (items, activeId, setActiveId, panelLabel) {
    var item = items.find(function (m) { return (m.id || m.cert_no) === activeId; }) || items[0] || {};
    var chemistry = item.chemistry || [];
    var mechanical = item.mechanical || [];
    var fields = [];
    Object.keys(item).forEach(function (k) {
      if (k !== "chemistry" && k !== "mechanical" && k !== "id") {
        fields.push([k.replace(/_/g, " "), item[k]]);
      }
    });

    var renderDataTable = function (data, label) {
      if (!data || data.length === 0) return null;
      return React.createElement("div", { style: { marginBottom: "10px" } },
        React.createElement("div", { style: { color: amber, fontSize: "8px", letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: "4px" } }, label),
        React.createElement("table", { style: { borderCollapse: "collapse", width: "100%", fontSize: "8.5px" } },
          React.createElement("thead", null,
            React.createElement("tr", { style: { background: "#111410" } },
              (Array.isArray(data[0]) ? data[0] : Object.keys(data[0])).map(function (hdr, hi) {
                return React.createElement("th", {
                  key: hi,
                  style: { padding: "4px 6px", textAlign: "left", color: amber, fontSize: "7px", letterSpacing: "0.06em", textTransform: "uppercase", borderBottom: "1px solid " + border, borderRight: "1px solid " + border, fontWeight: 600 }
                }, String(hdr));
              })
            )
          ),
          React.createElement("tbody", null,
            data.slice(1).map(function (row, ri) {
              var cells = Array.isArray(row) ? row : Object.values(row);
              return React.createElement("tr", { key: ri, style: { borderBottom: "1px solid " + border, background: ri % 2 === 0 ? "transparent" : "#1a1c18" } },
                cells.map(function (cell, ci) {
                  return React.createElement("td", {
                    key: ci,
                    style: { padding: "4px 6px", color: ri === 0 ? muted : textCol, fontSize: "8.5px", borderRight: "1px solid " + border }
                  }, String(cell || ""));
                })
              );
            })
          )
        )
      );
    };

    return React.createElement("div", null,
      React.createElement("div", { style: { display: "flex", gap: "4px", marginBottom: "10px", flexWrap: "wrap" } },
        items.map(function (m) {
          var mid = m.id || m.cert_no || "item";
          return React.createElement("button", {
            key: mid,
            onClick: function () { setActiveId(mid); },
            style: {
              background: activeId === mid ? "rgba(212,131,42,0.15)" : "none",
              border: "1px solid " + (activeId === mid ? amber : border),
              color: activeId === mid ? amber : muted,
              cursor: "pointer", padding: "5px 10px", fontFamily: mono,
              fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase"
            }
          }, m.cert_no || m.title || mid);
        })
      ),
      // Fields
      React.createElement("div", { style: { background: surf, border: "1px solid " + border, marginBottom: "10px" } },
        fields.map(function (pair, i) {
          return React.createElement("div", {
            key: i,
            style: {
              display: "grid", gridTemplateColumns: "160px 1fr",
              borderBottom: i < fields.length - 1 ? "1px solid " + border : "none"
            }
          },
            React.createElement("div", {
              style: { padding: "5px 10px", background: surf2, borderRight: "1px solid " + border, color: muted, fontSize: "8px", letterSpacing: "0.06em", textTransform: "uppercase", fontWeight: 600 }
            }, pair[0]),
            React.createElement("div", {
              style: { padding: "5px 10px", color: white, fontSize: "10px", wordBreak: "break-word" }
            }, Array.isArray(pair[1]) ? pair[1].join(", ") : (typeof pair[1] === "object" ? JSON.stringify(pair[1]) : String(pair[1] || "")))
          );
        })
      ),
      renderDataTable(chemistry, "Chemical Composition"),
      renderDataTable(mechanical, "Mechanical Properties")
    );
  };

  // ── Reference Panel ────────────────────────────────────────
  var renderRefPanel = function () {
    var refTabs = [
      ["weldmap", "Weld Map"],
      ["wps", "WPS Docs"],
      ["wqr", "WQRs"],
      ["travelers", "Travelers"],
      ["pipemtrs", "Pipe MTRs"],
      ["fillercerts", "Filler Certs"]
    ];
    return React.createElement("div", { style: { display: "flex", flexDirection: "column", height: "100%", overflow: "hidden" } },
      // Tab bar
      React.createElement("div", {
        style: { display: "flex", borderBottom: "1px solid " + border, flexShrink: 0, overflowX: "auto" }
      },
        refTabs.map(function (rt) {
          var rtId = rt[0], rtLabel = rt[1];
          return React.createElement("button", {
            key: rtId,
            onClick: function () { setRefTab(rtId); },
            style: {
              background: "none", border: "none",
              borderBottom: refTab === rtId ? "2px solid " + amber : "2px solid transparent",
              color: refTab === rtId ? amber : muted,
              cursor: "pointer", padding: "7px 10px", fontFamily: mono,
              fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase", whiteSpace: "nowrap"
            }
          }, rtLabel);
        })
      ),
      // Content
      React.createElement("div", { style: { flex: 1, overflowY: "auto", padding: "10px" } },
        refTab === "weldmap" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "6px" } },
            (CFG.scenario && CFG.scenario.system ? CFG.scenario.system : "System") + " \u00B7 Weld Location Map"
          ),
          React.createElement("div", { style: { background: "#080d0a", border: "1px solid " + border } }, renderWeldMap())
        ) : null,
        refTab === "wps" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "8px" } }, "Welding Procedure Specifications"),
          renderWpsDocs()
        ) : null,
        refTab === "wqr" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "8px" } }, "Welder Qualification Records"),
          renderWqrs()
        ) : null,
        refTab === "travelers" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "8px" } }, "Weld Travelers"),
          renderTravelers()
        ) : null,
        refTab === "pipemtrs" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "8px" } }, "Pipe Material Test Reports"),
          renderMtrPanel(pipeMtrs, activePipeMtr, setActivePipeMtr, "Pipe MTRs")
        ) : null,
        refTab === "fillercerts" ? React.createElement("div", null,
          React.createElement("div", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "8px" } }, "Filler Metal Certificates"),
          renderMtrPanel(fillerCerts, activeFillerCert, setActiveFillerCert, "Filler Certs")
        ) : null
      )
    );
  };

  // ── Single-weld form (Steps 1-3) ──────────────────────────
  var renderSingleWeldForm = function (stepId) {
    var fields = getFieldsForStep(stepId);
    var ans = answers[stepId] || {};
    var weldAns = ans["WLD-001"] || ans;
    var isSub = !!submitted[stepId];
    var sc = scores[stepId] || {};
    var pct = stepScores[stepId];
    var pass = !!stepPassed[stepId];
    var allFilled = fields.every(function (f) {
      return formData[stepId] && formData[stepId]["WLD-001"] && formData[stepId]["WLD-001"][f.key] && formData[stepId]["WLD-001"][f.key].trim() !== "";
    });

    // Group by section
    var sMap = {}, sOrder = [];
    fields.forEach(function (f) {
      var sec = f.section || "general";
      if (!sMap[sec]) { sMap[sec] = []; sOrder.push(sec); }
      sMap[sec].push(f);
    });

    var sectionColors = {
      weld_identification: amber,
      welding_procedure: "#8ab4c4",
      welder_qualification: "#a0c8a0",
      base_material: amber,
      filler_material: "#c4a882",
      preheat: "#8ab4c4",
      visual_inspection: "#a0c8a0",
      nde: amber,
      general: muted
    };

    return React.createElement("div", { style: { fontFamily: mono } },
      // Form header
      React.createElement("div", {
        style: { background: "rgba(212,131,42,0.08)", border: "1px solid " + border, borderTop: "2px solid " + amber, padding: "8px 12px", marginBottom: "12px" }
      },
        React.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start" } },
          React.createElement("div", null,
            React.createElement("div", { style: { color: amber, fontSize: "8px", letterSpacing: "0.18em", textTransform: "uppercase", marginBottom: "3px" } }, CFG.scenario && CFG.scenario.owner ? CFG.scenario.owner : ""),
            React.createElement("div", { style: { color: white, fontSize: "12px", fontWeight: 700, letterSpacing: "0.04em" } }, "WELD INSPECTION LOG"),
            React.createElement("div", { style: { color: muted, fontSize: "8px", marginTop: "2px" } }, currentStep.label || "Step")
          ),
          React.createElement("div", { style: { textAlign: "right" } },
            React.createElement("div", { style: { color: muted, fontSize: "7.5px", textTransform: "uppercase", letterSpacing: "0.1em" } }, "Weld"),
            React.createElement("div", { style: { color: amber, fontSize: "11px", fontWeight: 700 } }, "WLD-001"),
            React.createElement("div", { style: { color: muted, fontSize: "7.5px", marginTop: "2px" } }, welds[0] ? welds[0].description || "" : "")
          )
        ),
        React.createElement("div", {
          style: { marginTop: "8px", padding: "6px 8px", background: "rgba(0,0,0,0.3)", border: "1px solid " + border, fontSize: "8.5px", color: "#8ab4c4", fontStyle: "italic" }
        },
          React.createElement("span", { style: { color: "#8ab4c4", fontWeight: 700, marginRight: "6px" } }, "INSTRUCTIONS:"),
          currentStep.description || "Complete all fields using the reference documents in the right panel."
        )
      ),
      // Score banner
      isSub ? React.createElement("div", {
        style: {
          background: pass ? "rgba(82,163,102,0.1)" : "rgba(201,95,95,0.08)",
          border: "1px solid " + (pass ? "rgba(82,163,102,0.3)" : "rgba(201,95,95,0.3)"),
          padding: "9px 12px", marginBottom: "12px",
          display: "flex", justifyContent: "space-between", alignItems: "center"
        }
      },
        React.createElement("span", { style: { color: pass ? green : red, fontWeight: 700, fontSize: "12px" } },
          currentStep.label + " ", pass ? "\u2713 PASSED" : "\u2717 NOT PASSED", " \u2014 ", pct, "%",
          React.createElement("span", { style: { color: muted, fontSize: "9px", fontWeight: 400, marginLeft: "8px" } },
            pass ? "Min. 80% required." : "Correct answers shown in green below."
          )
        ),
        React.createElement("div", { style: { display: "flex", gap: "8px" } },
          !pass ? React.createElement("button", {
            onClick: function () { handleRetry(stepId); },
            style: { background: "none", border: "1px solid " + border, color: muted, padding: "5px 10px", cursor: "pointer", fontFamily: mono, fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase" }
          }, "Retry") : null,
          pass && stepIndex(stepId) < steps.length - 1 ? React.createElement("button", {
            onClick: function () { setActiveStep(steps[stepIndex(stepId) + 1].id); },
            style: { background: amber, color: bg, border: "none", padding: "7px 14px", cursor: "pointer", fontFamily: mono, fontSize: "9px", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 700 }
          }, "Proceed to Next Step \u2192") : null,
          pass && stepIndex(stepId) === steps.length - 1 ? React.createElement("button", {
            onClick: handleExerciseComplete,
            style: { background: green, color: bg, border: "none", padding: "7px 14px", cursor: "pointer", fontFamily: mono, fontSize: "9px", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 700 }
          }, "Exercise Complete \u2713") : null
        )
      ) : null,
      // Weld identification bar
      React.createElement("div", {
        style: { border: "1px solid " + border, marginBottom: "8px", background: surf }
      },
        React.createElement("div", { style: { padding: "5px 10px", background: "rgba(255,255,255,0.03)", borderBottom: "1px solid " + border } },
          React.createElement("span", { style: { color: muted, fontSize: "7.5px", letterSpacing: "0.14em", textTransform: "uppercase" } },
            "Weld Identification ",
            React.createElement("span", { style: { color: muted, marginLeft: "8px" } }, "(from Weld Map \u2014 pre-populated)")
          )
        ),
        React.createElement("div", { style: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr" } },
          [
            ["Weld ID", welds[0] ? welds[0].id : "WLD-001"],
            ["Type", welds[0] ? welds[0].type || "" : ""],
            ["Size", welds[0] ? welds[0].size || "" : ""],
            ["Joint Type", welds[0] ? welds[0].joint_type || "" : ""]
          ].map(function (pair, i) {
            return React.createElement("div", {
              key: pair[0],
              style: { padding: "6px 10px", borderRight: i < 3 ? "1px solid " + border : "none" }
            },
              React.createElement("div", { style: { color: muted, fontSize: "7px", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "2px" } }, pair[0]),
              React.createElement("div", { style: { color: "#4a6a52", fontSize: "10px", fontWeight: 600 } }, pair[1])
            );
          })
        )
      ),
      // Section-grouped fields
      sOrder.map(function (secKey) {
        var secFields = sMap[secKey];
        var secColor = sectionColors[secKey] || muted;
        return React.createElement("div", {
          key: secKey,
          style: { border: "1px solid " + border, marginBottom: "8px", background: surf }
        },
          React.createElement("div", {
            style: { padding: "5px 10px", background: "rgba(255,255,255,0.03)", borderBottom: "1px solid " + border, borderLeft: "2px solid " + secColor }
          },
            React.createElement("span", { style: { color: secColor, fontSize: "7.5px", letterSpacing: "0.14em", textTransform: "uppercase" } },
              secKey.replace(/_/g, " ")
            )
          ),
          React.createElement("div", null,
            secFields.map(function (field, fi) {
              return React.createElement("div", {
                key: field.key,
                style: {
                  display: "grid", gridTemplateColumns: "200px 1fr",
                  borderBottom: fi < secFields.length - 1 ? "1px solid #1a1c18" : "none"
                }
              },
                // Label column
                React.createElement("div", {
                  style: { padding: "6px 10px", background: surf2, borderRight: "1px solid " + border }
                },
                  React.createElement("div", { style: { display: "flex", alignItems: "center" } },
                    React.createElement("span", {
                      style: { color: textCol, fontSize: "7.5px", letterSpacing: "0.07em", textTransform: "uppercase", fontWeight: 600 }
                    }, field.label),
                    field.tooltip && !isSub ? React.createElement("span", { className: "tip-wrap" },
                      React.createElement("span", { className: "tip-icon" }, "i"),
                      React.createElement("span", { className: "tip-box" }, field.tooltip)
                    ) : null
                  ),
                  React.createElement("div", {
                    style: { color: "#8a9ea8", fontSize: "7px", lineHeight: 1.5, fontStyle: "italic", marginTop: "3px" }
                  }, field.hint || "")
                ),
                // Input column — IIFE to avoid focus loss
                React.createElement("div", null, (function () {
                  var ck = "WLD-001|" + field.key;
                  var fr = isSub && sc["WLD-001"] && sc["WLD-001"][field.key];
                  var wrapStyle = isSub
                    ? { outline: "1.5px solid " + (fr && fr.ok ? "rgba(82,163,102,0.4)" : "rgba(201,95,95,0.35)"), background: fr && fr.ok ? "rgba(82,163,102,0.08)" : "rgba(201,95,95,0.08)" }
                    : { outline: "1px solid #2a4a2a", background: "rgba(42,74,42,0.08)", transition: "outline 0.15s" };
                  return React.createElement("div", { className: "fdq-form-input-wrap", style: wrapStyle },
                    React.createElement("input", {
                      className: "fdq-form-input",
                      ref: function (el) { if (el) inputRefs.current[stepId + "|" + ck] = el; },
                      value: (formData[stepId] && formData[stepId]["WLD-001"] && formData[stepId]["WLD-001"][field.key]) || "",
                      disabled: isSub,
                      onChange: function (e) { updateField(stepId, "WLD-001", field.key, e.target.value); },
                      placeholder: field.hint || "",
                      style: {
                        width: "100%", background: "transparent", border: "none", outline: "none",
                        color: isSub ? (fr && fr.ok ? "#52a366" : "#c95f5f") : "#ede8df",
                        padding: "5px 8px", fontSize: "10px", fontFamily: mono,
                        cursor: isSub ? "default" : "text", boxSizing: "border-box"
                      }
                    }),
                    isSub && fr && !fr.ok
                      ? React.createElement("div", { style: { padding: "0 8px 4px", fontSize: "8px", color: "#52a366" } }, "\u2713 " + fr.correct)
                      : null
                  );
                })())
              );
            })
          )
        );
      }),
      // Submit bar
      !isSub ? React.createElement("div", {
        style: { display: "flex", justifyContent: "space-between", alignItems: "center" }
      },
        React.createElement("span", { style: { color: muted, fontSize: "8px" } },
          allFilled ? "All fields complete \u2014 ready to submit." : "Complete all fields to submit."
        ),
        React.createElement("button", {
          onClick: function () { handleSubmitStep(stepId); },
          disabled: !allFilled,
          style: {
            background: allFilled ? amber : "#232520",
            color: allFilled ? bg : "#3d3f39",
            border: "none", padding: "10px 22px",
            cursor: allFilled ? "pointer" : "not-allowed",
            fontFamily: mono, fontSize: "11px", letterSpacing: "0.12em",
            textTransform: "uppercase", fontWeight: 600
          }
        }, "Submit Step")
      ) : null
    );
  };

  // ── All-weld table (Steps 4-5) ────────────────────────────
  var renderAllWeldTable = function (stepId) {
    var fields = getFieldsForStep(stepId);
    var isSub = !!submitted[stepId];
    var sc = scores[stepId] || {};
    var pct = stepScores[stepId];
    var pass = !!stepPassed[stepId];
    var allFilled = welds.every(function (w) {
      return fields.every(function (f) {
        return formData[stepId] && formData[stepId][w.id] && formData[stepId][w.id][f.key] && formData[stepId][w.id][f.key].trim() !== "";
      });
    });

    return React.createElement("div", { style: { fontFamily: mono } },
      // Header info block
      React.createElement("div", {
        style: { background: surf, border: "1px solid " + border, borderTop: "2px solid " + amber, padding: "10px 12px", marginBottom: "10px", display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "8px" }
      },
        [
          ["Project", CFG.scenario ? CFG.scenario.project || "" : ""],
          ["System", CFG.scenario ? CFG.scenario.system || "" : ""],
          ["Step", currentStep.label || ""],
          ["Code", CFG.scenario ? CFG.scenario.code || "" : ""],
          ["Service", CFG.scenario ? CFG.scenario.service || "" : ""],
          ["Date", "___________"]
        ].map(function (pair) {
          return React.createElement("div", { key: pair[0] },
            React.createElement("div", { style: { color: amber, fontSize: "7px", letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: "1px" } }, pair[0]),
            React.createElement("div", { style: { color: white, fontSize: "10px" } }, pair[1])
          );
        })
      ),
      // Score banner
      isSub ? React.createElement("div", {
        style: {
          background: pass ? "rgba(82,163,102,0.12)" : "rgba(201,95,95,0.1)",
          border: "1px solid " + (pass ? "rgba(82,163,102,0.35)" : "rgba(201,95,95,0.3)"),
          padding: "9px 12px", marginBottom: "10px",
          display: "flex", justifyContent: "space-between", alignItems: "center"
        }
      },
        React.createElement("span", { style: { color: pass ? green : red, fontWeight: 700, fontSize: "12px" } },
          pass ? "\u2713 PASSED" : "\u2717 NOT PASSED", " \u2014 ", pct, "%",
          React.createElement("span", { style: { color: muted, fontSize: "10px", fontWeight: 400, marginLeft: "8px" } },
            pass ? "Min. 80% required." : "Correct answers shown below cells."
          )
        ),
        React.createElement("div", { style: { display: "flex", gap: "8px" } },
          !pass ? React.createElement("button", {
            onClick: function () { handleRetry(stepId); },
            style: { background: "none", border: "1px solid " + border, color: muted, padding: "5px 10px", cursor: "pointer", fontFamily: mono, fontSize: "9px", letterSpacing: "0.1em", textTransform: "uppercase" }
          }, "Retry") : null,
          pass && stepIndex(stepId) < steps.length - 1 ? React.createElement("button", {
            onClick: function () { setActiveStep(steps[stepIndex(stepId) + 1].id); },
            style: { background: amber, color: bg, border: "none", padding: "7px 14px", cursor: "pointer", fontFamily: mono, fontSize: "9px", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 700 }
          }, "Next Step \u2192") : null,
          pass && stepIndex(stepId) === steps.length - 1 ? React.createElement("button", {
            onClick: handleExerciseComplete,
            style: { background: green, color: bg, border: "none", padding: "7px 14px", cursor: "pointer", fontFamily: mono, fontSize: "9px", letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 700 }
          }, "Exercise Complete \u2713") : null
        )
      ) : null,
      // Table
      React.createElement("div", { style: { overflowX: "auto", background: surf, border: "1px solid " + border } },
        React.createElement("table", { style: { borderCollapse: "collapse", fontSize: "11px", width: "100%" } },
          // Thead
          React.createElement("thead", null,
            React.createElement("tr", { style: { background: surf2 } },
              // Weld ID column
              React.createElement("th", {
                style: { padding: "7px 8px", textAlign: "left", color: muted, fontSize: "8px", letterSpacing: "0.08em", textTransform: "uppercase", borderBottom: "2px solid " + border, borderRight: "1px solid " + border, fontWeight: 500, whiteSpace: "nowrap" }
              }, "Weld"),
              // Weld description column
              React.createElement("th", {
                style: { padding: "7px 8px", textAlign: "left", color: muted, fontSize: "8px", letterSpacing: "0.08em", textTransform: "uppercase", borderBottom: "2px solid " + border, borderRight: "1px solid " + border, fontWeight: 500, whiteSpace: "nowrap" }
              }, "Description"),
              // Input columns
              fields.map(function (col, ci) {
                return React.createElement("th", {
                  key: col.key,
                  style: { padding: "7px 8px", textAlign: "left", color: amber, fontSize: "8px", letterSpacing: "0.08em", textTransform: "uppercase", borderBottom: "2px solid " + amber, borderRight: ci < fields.length - 1 ? "1px solid " + border : "none", fontWeight: 600, whiteSpace: "pre-line", minWidth: "72px" }
                }, col.label);
              })
            )
          ),
          // Tbody
          React.createElement("tbody", null,
            welds.map(function (w, ri) {
              return React.createElement("tr", {
                key: w.id,
                style: { borderBottom: "1px solid " + border, background: ri % 2 === 0 ? "transparent" : "#1a1c18" }
              },
                // Weld ID cell
                React.createElement("td", {
                  style: { padding: "0 8px", height: "42px", color: amber, fontWeight: 600, borderRight: "1px solid " + border, whiteSpace: "nowrap", fontSize: "11px" }
                }, w.id),
                // Description cell
                React.createElement("td", {
                  style: { padding: "0 8px", color: textCol, fontSize: "11px", borderRight: "1px solid " + border, whiteSpace: "nowrap" }
                }, w.description || w.type || ""),
                // Input cells
                fields.map(function (col, ci) {
                  var ck = w.id + "|" + col.key;
                  var fr = isSub && sc[w.id] && sc[w.id][col.key];
                  var outlineColor = "transparent", cellBg = "transparent";
                  if (activeCell === stepId + "|" + ck && !isSub) {
                    outlineColor = amber;
                    cellBg = "rgba(212,131,42,0.08)";
                  }
                  if (isSub) {
                    cellBg = fr && fr.ok ? "rgba(82,163,102,0.1)" : "rgba(201,95,95,0.08)";
                    outlineColor = fr && fr.ok ? "rgba(82,163,102,0.4)" : "rgba(201,95,95,0.4)";
                  }
                  return React.createElement("td", {
                    key: col.key,
                    style: { padding: 0, borderRight: ci < fields.length - 1 ? "1px solid " + border : "none" }
                  },
                    React.createElement("div", {
                      style: { outline: "2px solid " + outlineColor, outlineOffset: "-2px", background: cellBg, minHeight: "42px", display: "flex", flexDirection: "column", justifyContent: "center" }
                    },
                      React.createElement("input", {
                        ref: function (el) { if (el) inputRefs.current[stepId + "|" + ck] = el; },
                        value: (formData[stepId] && formData[stepId][w.id] && formData[stepId][w.id][col.key]) || "",
                        disabled: isSub,
                        onChange: function (e) { updateField(stepId, w.id, col.key, e.target.value); },
                        onFocus: function () { setActiveCell(stepId + "|" + ck); },
                        onBlur: function () { setActiveCell(null); },
                        onKeyDown: function (e) {
                          if (e.key === "Tab" || e.key === "Enter") {
                            e.preventDefault();
                            navToNext(stepId, ck);
                          }
                        },
                        placeholder: col.hint || "",
                        style: {
                          width: "100%", background: "transparent", border: "none", outline: "none",
                          color: isSub ? (fr && fr.ok ? green : red) : white,
                          padding: "8px", fontSize: "11px", fontFamily: mono,
                          cursor: isSub ? "default" : "text", boxSizing: "border-box"
                        }
                      }),
                      isSub && fr && !fr.ok ? React.createElement("div", {
                        style: { padding: "0 8px 5px", fontSize: "8px", color: green, letterSpacing: "0.06em" }
                      }, "\u2713 " + fr.correct) : null
                    )
                  );
                })
              );
            })
          )
        )
      ),
      // Footer
      React.createElement("div", { style: { color: "#3d3f39", fontSize: "8px", marginTop: "5px", letterSpacing: "0.1em" } }, "TAB or ENTER to advance"),
      React.createElement("div", { style: { marginTop: "14px", display: "flex", justifyContent: "flex-end", gap: "10px", alignItems: "center" } },
        !isSub && !allFilled ? React.createElement("span", { style: { color: muted, fontSize: "9px" } }, "Fill all cells to submit") : null,
        !isSub ? React.createElement(Btn, {
          onClick: function () { handleSubmitStep(stepId); },
          disabled: !allFilled
        }, "Submit Step") : null
      )
    );
  };

  // ── Determine which form pane to render ────────────────────
  var renderFormPane = function () {
    if (!currentStep.id) return null;
    if (currentStep.scope === "single") {
      return renderSingleWeldForm(activeStep);
    } else {
      return renderAllWeldTable(activeStep);
    }
  };

  // ── Overall score display ──────────────────────────────────
  var overallScore = null;
  var overallPassed = false;
  var completedSteps = steps.filter(function (s) { return submitted[s.id]; });
  if (completedSteps.length > 0) {
    var totalPct = 0;
    completedSteps.forEach(function (s) { totalPct += (stepScores[s.id] || 0); });
    overallScore = Math.round(totalPct / completedSteps.length);
    overallPassed = completedSteps.length === steps.length && steps.every(function (s) { return stepPassed[s.id]; });
  }

  // ── MAIN RENDER ────────────────────────────────────────────
  return React.createElement("div", {
    style: { fontFamily: mono, background: bg, color: textCol, height: "100vh", display: "flex", flexDirection: "column", fontSize: "13px" }
  },
    // ── Header bar ─────────────────────────────────────────────
    React.createElement("div", {
      style: { background: surf, borderBottom: "1px solid " + border, padding: "10px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", flexShrink: 0 }
    },
      React.createElement("div", null,
        React.createElement("div", { style: { color: amber, fontSize: "8px", letterSpacing: "0.2em", textTransform: "uppercase", marginBottom: "2px" } }, "FDQ Tier 1 \u00B7 Practical Exercise"),
        React.createElement("div", { style: { color: white, fontSize: "16px", fontWeight: 900, textTransform: "uppercase", letterSpacing: "0.06em" } }, "Weld Inspection Log")
      ),
      React.createElement("div", { style: { display: "flex", alignItems: "center", gap: "16px" } },
        overallScore !== null ? React.createElement("div", { style: { textAlign: "right" } },
          React.createElement("div", { style: { fontSize: "28px", fontWeight: 900, color: overallPassed ? green : completedSteps.length > 0 ? amber : muted, lineHeight: 1 } }, overallScore, "%"),
          React.createElement("div", { style: { fontSize: "8px", color: overallPassed ? green : muted, letterSpacing: "0.14em", textTransform: "uppercase" } },
            overallPassed ? "\u2713 ALL PASSED" : completedSteps.length + "/" + steps.length + " STEPS"
          )
        ) : null,
        React.createElement("div", { style: { display: "flex", borderLeft: "1px solid " + border, paddingLeft: "16px", gap: "4px" } },
          [["brief", "Scenario"], ["work", "Work View"]].map(function (pair) {
            var id = pair[0], label = pair[1];
            return React.createElement("button", {
              key: id,
              onClick: function () { setTab(id); },
              style: {
                background: tab === id ? "rgba(212,131,42,0.12)" : "none",
                border: "1px solid " + (tab === id ? amber : border),
                color: tab === id ? amber : muted,
                cursor: "pointer", padding: "6px 14px", fontFamily: mono,
                fontSize: "9px", letterSpacing: "0.12em", textTransform: "uppercase"
              }
            }, label);
          })
        )
      )
    ),
    // ── Brief tab ──────────────────────────────────────────────
    tab === "brief" ? React.createElement("div", {
      style: { flex: 1, overflowY: "auto", padding: "20px", maxWidth: "860px", margin: "0 auto", width: "100%" }
    },
      // Brief box
      React.createElement("div", {
        style: { background: surf, border: "1px solid " + border, borderLeft: "3px solid " + amber, padding: "18px 20px", marginBottom: "16px" }
      },
        React.createElement("div", { style: { color: amber, fontSize: "9px", letterSpacing: "0.2em", textTransform: "uppercase", marginBottom: "10px" } }, "Exercise Brief"),
        React.createElement("p", { style: { fontFamily: "sans-serif", fontSize: "14px", lineHeight: 1.85, margin: 0 } },
          "You are the QC Inspector on ",
          React.createElement("strong", { style: { color: white } }, CFG.scenario ? CFG.scenario.project || "" : ""),
          ". Welding for ",
          React.createElement("strong", { style: { color: white } }, CFG.scenario ? CFG.scenario.system || "" : ""),
          " is complete. Switch to ",
          React.createElement("strong", { style: { color: white } }, "Work View"),
          " to access the weld map, WPS documents, welder qualifications, weld travelers, and material test reports \u2014 all alongside the fillable inspection log. Complete each step in sequence: review weld data, verify procedures, confirm materials, then inspect all welds. Inspector: ",
          React.createElement("strong", { style: { color: white } }, CFG.scenario ? CFG.scenario.inspector || "Inspector" : "Inspector"),
          "."
        )
      ),
      // Scenario info grid
      React.createElement("div", {
        style: { background: surf, border: "1px solid " + border, display: "grid", gridTemplateColumns: "1fr 1fr", marginBottom: "20px" }
      },
        [
          ["Project", CFG.scenario ? CFG.scenario.project || "" : ""],
          ["System", CFG.scenario ? CFG.scenario.system || "" : ""],
          ["Code", CFG.scenario ? CFG.scenario.code || "" : ""],
          ["Service", CFG.scenario ? CFG.scenario.service || "" : ""],
          ["Contractor", CFG.scenario ? CFG.scenario.contractor || "" : ""],
          ["Inspector", CFG.scenario ? CFG.scenario.inspector || "" : ""],
          ["Total Welds", String(welds.length)],
          ["Steps", String(steps.length)]
        ].map(function (pair, i) {
          return React.createElement("div", {
            key: pair[0],
            style: { padding: "10px 14px", borderBottom: "1px solid " + border, borderRight: i % 2 === 0 ? "1px solid " + border : "none", display: "flex", gap: "12px" }
          },
            React.createElement("div", { style: { color: amber, fontSize: "8px", letterSpacing: "0.1em", textTransform: "uppercase", width: "120px", flexShrink: 0 } }, pair[0]),
            React.createElement("div", { style: { color: white, fontSize: "12px" } }, pair[1])
          );
        })
      ),
      // 5-weld summary table
      React.createElement("div", {
        style: { background: surf, border: "1px solid " + border, marginBottom: "20px" }
      },
        React.createElement("div", { style: { padding: "8px 12px", background: surf2, borderBottom: "1px solid " + border } },
          React.createElement("span", { style: { color: amber, fontSize: "8px", letterSpacing: "0.14em", textTransform: "uppercase" } }, "Weld Summary")
        ),
        React.createElement("table", { style: { borderCollapse: "collapse", width: "100%", fontSize: "10px" } },
          React.createElement("thead", null,
            React.createElement("tr", { style: { background: "#111410" } },
              ["Weld ID", "Type", "Size", "Joint", "WPS", "Welder"].map(function (h, hi) {
                return React.createElement("th", {
                  key: h,
                  style: { padding: "6px 10px", textAlign: "left", color: amber, fontSize: "7.5px", letterSpacing: "0.08em", textTransform: "uppercase", borderBottom: "1px solid " + border, borderRight: hi < 5 ? "1px solid " + border : "none", fontWeight: 600 }
                }, h);
              })
            )
          ),
          React.createElement("tbody", null,
            welds.map(function (w, ri) {
              return React.createElement("tr", {
                key: w.id,
                style: { borderBottom: "1px solid " + border, background: ri % 2 === 0 ? "transparent" : "#1a1c18" }
              },
                React.createElement("td", { style: { padding: "5px 10px", color: amber, fontWeight: 600, borderRight: "1px solid " + border } }, w.id),
                React.createElement("td", { style: { padding: "5px 10px", color: textCol, borderRight: "1px solid " + border } }, w.type || ""),
                React.createElement("td", { style: { padding: "5px 10px", color: textCol, borderRight: "1px solid " + border } }, w.size || ""),
                React.createElement("td", { style: { padding: "5px 10px", color: textCol, borderRight: "1px solid " + border } }, w.joint_type || ""),
                React.createElement("td", { style: { padding: "5px 10px", color: textCol, borderRight: "1px solid " + border } }, w.wps || ""),
                React.createElement("td", { style: { padding: "5px 10px", color: textCol } }, w.welder || "")
              );
            })
          )
        )
      ),
      React.createElement(Btn, { onClick: function () { setTab("work"); } }, "Open Work View \u2192")
    ) : null,
    // ── Work View ──────────────────────────────────────────────
    tab === "work" ? React.createElement("div", {
      style: { flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }
    },
      // Step indicator bar
      React.createElement("div", {
        style: { display: "flex", background: surf2, borderBottom: "1px solid " + border, flexShrink: 0, padding: "0 16px", overflowX: "auto" }
      },
        steps.map(function (st, i) {
          var unlocked = isStepUnlocked(st.id);
          var isActive = activeStep === st.id;
          return React.createElement("div", {
            key: st.id,
            onClick: function () {
              if (unlocked) setActiveStep(st.id);
            },
            style: {
              display: "flex", alignItems: "center", gap: "8px", padding: "8px 14px",
              cursor: unlocked ? "pointer" : "not-allowed",
              opacity: unlocked ? 1 : 0.35,
              borderBottom: isActive ? "2px solid " + amber : "2px solid transparent",
              marginBottom: "-1px", whiteSpace: "nowrap"
            }
          },
            // Step number circle
            React.createElement("div", {
              style: {
                width: "18px", height: "18px", borderRadius: "50%",
                background: isActive ? "rgba(212,131,42,0.2)" : stepPassed[st.id] ? "rgba(82,163,102,0.2)" : "transparent",
                border: "1px solid " + (isActive ? amber : stepPassed[st.id] ? green : border),
                display: "flex", alignItems: "center", justifyContent: "center"
              }
            },
              React.createElement("span", {
                style: { color: isActive ? amber : stepPassed[st.id] ? green : muted, fontSize: "8px", fontWeight: 700 }
              }, stepPassed[st.id] ? "\u2713" : String(i + 1))
            ),
            // Step label
            React.createElement("div", null,
              React.createElement("div", {
                style: { color: isActive ? amber : stepPassed[st.id] ? green : muted, fontSize: "8.5px", fontWeight: 700, letterSpacing: "0.06em" }
              }, "Step " + (i + 1) + " of " + steps.length),
              React.createElement("div", { style: { color: "#3a3d37", fontSize: "7px", letterSpacing: "0.04em" } }, st.label || "")
            ),
            i < steps.length - 1 ? React.createElement("div", { style: { color: border, fontSize: "12px", marginLeft: "6px" } }, "\u203A") : null
          );
        })
      ),
      // Split pane: 52% form / 48% ref
      React.createElement("div", { style: { flex: 1, display: "flex", overflow: "hidden" } },
        // Left pane: form
        React.createElement("div", {
          style: { width: "52%", borderRight: "1px solid " + border, display: "flex", flexDirection: "column", overflow: "hidden" }
        },
          // Form header
          React.createElement("div", {
            style: { padding: "7px 12px", background: surf2, borderBottom: "1px solid " + border, flexShrink: 0 }
          },
            React.createElement("span", {
              style: { color: muted, fontSize: "8px", letterSpacing: "0.14em", textTransform: "uppercase" }
            }, (currentStep.label || "Step") + " \u00B7 " + (currentStep.scope === "single" ? "WLD-001" : "All Welds"))
          ),
          // Form content
          React.createElement("div", { style: { flex: 1, overflowY: "auto", padding: "12px" } },
            renderFormPane()
          )
        ),
        // Right pane: reference panel
        React.createElement("div", {
          style: { flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }
        },
          React.createElement("div", {
            style: { padding: "7px 12px", background: surf2, borderBottom: "1px solid " + border, flexShrink: 0 }
          },
            React.createElement("span", {
              style: { color: muted, fontSize: "8px", letterSpacing: "0.14em", textTransform: "uppercase" }
            }, "Reference \u00B7 Scenario Documents")
          ),
          React.createElement("div", { style: { flex: 1, overflow: "hidden" } },
            renderRefPanel()
          )
        )
      )
    ) : null
  );
}

(function() {
  var mountEl = document.getElementById('exercise-root') || document.getElementById('root');
  var root = ReactDOM.createRoot(mountEl);
  var exerciseType = window.EXERCISE_TYPE || 'torque_form';
  if (exerciseType === 'weld_log') {
    root.render(React.createElement(WeldLog));
  } else {
    root.render(React.createElement(TorqueLog));
  }
})();
