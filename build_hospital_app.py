# build_hospital_app.py
import re

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>City General Hospital - High Quality 3D Interactive Walkthrough</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #070a12;
      --panel-bg: rgba(13, 19, 33, 0.92);
      --panel-border: rgba(255, 255, 255, 0.12);
      --accent-blue: #2563eb;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-rose: #f43f5e;
      --accent-amber: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
    }

    #webgl-container {
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
      outline: none;
    }

    /* TOP HEADER */
    .top-bar {
      position: absolute;
      top: 14px;
      left: 18px;
      right: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      pointer-events: none;
      z-index: 30;
      gap: 12px;
    }

    .brand-card {
      pointer-events: auto;
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--panel-border);
      border-radius: 14px;
      padding: 10px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 10px 35px rgba(0,0,0,0.5);
    }

    .brand-logo {
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, #2563eb, #0284c7);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 24px;
      color: white;
      box-shadow: 0 4px 14px rgba(37,99,235,0.4);
    }

    .brand-info h1 {
      font-size: 15px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #fff;
    }

    .brand-info p {
      font-size: 11px;
      color: #38bdf8;
      font-weight: 600;
    }

    /* LOCATION HUD BANNER */
    .location-hud {
      pointer-events: auto;
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 30px;
      padding: 8px 22px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.5);
      transition: all 0.3s ease;
    }

    .location-hud.active-room {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 25px rgba(6, 182, 212, 0.5);
      transform: scale(1.02);
    }

    .loc-icon {
      font-size: 16px;
      animation: pulse 1.6s infinite;
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.2); }
    }

    .loc-text {
      font-size: 13px;
      font-weight: 700;
      color: #fff;
    }

    .loc-floor {
      background: rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 12px;
      font-family: 'JetBrains Mono', monospace;
      border: 1px solid rgba(56, 189, 248, 0.4);
    }

    /* TOP ACTIONS */
    .top-actions {
      pointer-events: auto;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn-action {
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--panel-border);
      color: var(--text-main);
      padding: 8px 13px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .btn-action:hover {
      background: rgba(30, 41, 59, 0.95);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-1px);
    }

    .btn-action.active {
      background: rgba(6, 182, 212, 0.25);
      border-color: var(--accent-cyan);
      color: #38bdf8;
    }

    .btn-primary {
      background: linear-gradient(135deg, #10b981, #059669);
      border: none;
      color: white;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(16,185,129,0.3);
    }

    .btn-primary:hover {
      background: linear-gradient(135deg, #059669, #047857);
    }

    /* LEFT CONTROLS DOCK */
    .left-dock {
      position: absolute;
      top: 80px;
      left: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      z-index: 25;
      max-height: calc(100vh - 100px);
      overflow-y: auto;
      scrollbar-width: thin;
      scrollbar-color: rgba(255,255,255,0.2) transparent;
      padding-bottom: 20px;
    }

    .dock-panel {
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--panel-border);
      border-radius: 14px;
      padding: 12px 14px;
      width: 240px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .dock-panel h3 {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .pill-group {
      display: grid;
      grid-template-columns: 1fr;
      gap: 5px;
    }

    .pill-btn {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      color: var(--text-main);
      padding: 7px 10px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      text-align: left;
    }

    .pill-btn:hover {
      background: rgba(255,255,255,0.12);
      border-color: rgba(255,255,255,0.25);
    }

    .pill-btn.active {
      background: linear-gradient(135deg, rgba(37,99,235,0.4), rgba(6,182,212,0.4));
      border-color: var(--accent-cyan);
      color: #38bdf8;
      font-weight: 600;
    }

    .pill-icon {
      font-size: 14px;
    }

    /* RADAR MINIMAP (TOP RIGHT) */
    .minimap-container {
      position: absolute;
      top: 80px;
      right: 18px;
      width: 250px;
      height: 180px;
      background: rgba(13, 19, 33, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 10px 35px rgba(0,0,0,0.6);
      z-index: 25;
      display: flex;
      flex-direction: column;
    }

    .minimap-header {
      padding: 6px 12px;
      background: rgba(24, 33, 54, 0.9);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      font-weight: 700;
      color: #94a3b8;
    }

    .minimap-header span strong {
      color: #38bdf8;
    }

    #minimap-canvas {
      width: 100%;
      height: 100%;
      background: #080c16;
    }

    /* ELEVATOR MODAL */
    .elevator-modal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0.9);
      width: 330px;
      background: var(--panel-bg);
      backdrop-filter: blur(24px);
      border: 2px solid var(--accent-cyan);
      border-radius: 18px;
      padding: 24px;
      z-index: 100;
      box-shadow: 0 20px 60px rgba(0,0,0,0.85);
      display: none;
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      text-align: center;
    }

    .elevator-modal.open {
      display: block;
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }

    .elevator-modal h2 {
      font-size: 18px;
      margin-bottom: 6px;
      color: #fff;
    }

    .elevator-modal p {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 20px;
    }

    .elevator-buttons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .elev-floor-btn {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 12px;
      padding: 16px 10px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }

    .elev-floor-btn:hover {
      background: rgba(6, 182, 212, 0.2);
      border-color: var(--accent-cyan);
      transform: translateY(-2px);
    }

    .elev-floor-btn .elev-num {
      font-size: 30px;
      font-weight: 800;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }

    .elev-floor-btn .elev-sub {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }

    .elev-floor-btn.current {
      border-color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.15);
    }

    .elev-floor-btn.current .elev-num {
      color: var(--accent-emerald);
    }

    /* INTERACTION PROMPT */
    .interaction-prompt {
      position: absolute;
      top: 60%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(13, 19, 33, 0.95);
      border: 1px solid var(--accent-cyan);
      border-radius: 10px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 700;
      color: #38bdf8;
      box-shadow: 0 6px 25px rgba(0,0,0,0.6);
      z-index: 35;
      display: none;
      animation: bounce 1s infinite alternate;
    }

    @keyframes bounce {
      from { transform: translate(-50%, -50%) translateY(0); }
      to { transform: translate(-50%, -50%) translateY(-6px); }
    }

    /* CONTROLS HUD */
    .controls-hud {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--panel-border);
      border-radius: 30px;
      padding: 8px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      z-index: 25;
      font-size: 12px;
      color: #cbd5e1;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      white-space: nowrap;
    }

    .key-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 6px;
      padding: 2px 7px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: #fff;
      box-shadow: 0 2px 0 rgba(0,0,0,0.4);
      margin-right: 4px;
    }

    /* RIGHT ROOM DETAIL DRAWER */
    .right-drawer {
      position: absolute;
      top: 275px;
      right: 18px;
      width: 290px;
      background: var(--panel-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--panel-border);
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.6);
      z-index: 25;
      display: none;
    }

    .right-drawer.open {
      display: block;
      animation: fadeIn 0.25s forwards;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .room-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: rgba(59,130,246,0.2);
      color: #60a5fa;
      border: 1px solid rgba(59,130,246,0.4);
    }

    .close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 16px;
    }

    .close-btn:hover { color: #fff; }

    .room-title {
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 3px;
      color: #fff;
    }

    .room-category {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .dot-indicator {
      width: 7px;
      height: 7px;
      border-radius: 50%;
    }

    .detail-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 12px;
    }

    .detail-card {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 8px;
      padding: 6px 8px;
    }

    .detail-card .label {
      font-size: 9px;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 2px;
    }

    .detail-card .val {
      font-size: 12px;
      font-weight: 600;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }

    .equipment-list {
      background: rgba(255,255,255,0.02);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 8px;
      padding: 8px;
      font-size: 11px;
      line-height: 1.4;
      color: #cbd5e1;
    }

    .equipment-list h4 {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }

    /* ON-SCREEN VIRTUAL DPAD */
    .virtual-dpad {
      position: absolute;
      bottom: 24px;
      left: 24px;
      width: 120px;
      height: 120px;
      z-index: 30;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(3, 1fr);
      gap: 4px;
    }

    .dpad-btn {
      background: rgba(13, 19, 33, 0.75);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 10px;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      cursor: pointer;
      touch-action: manipulation;
    }

    .dpad-btn:active {
      background: rgba(6, 182, 212, 0.4);
      border-color: var(--accent-cyan);
    }

    /* HOSPITAL DIRECTORY & SEARCH MODAL */
    .directory-modal-backdrop {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(4, 7, 15, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 120;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }

    .directory-modal-backdrop.open {
      opacity: 1;
      pointer-events: auto;
    }

    .directory-modal {
      width: 90%;
      max-width: 920px;
      max-height: 85vh;
      background: var(--panel-bg);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 20px;
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transform: scale(0.95);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .directory-modal-backdrop.open .directory-modal {
      transform: scale(1);
    }

    .dir-header {
      padding: 20px 24px 14px;
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.6);
    }

    .dir-title-area h2 {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .dir-title-area p {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 3px;
    }

    .dir-search-bar {
      padding: 14px 24px;
      background: rgba(10, 15, 28, 0.95);
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .search-input-wrap {
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
    }

    .search-icon {
      position: absolute;
      left: 14px;
      color: #38bdf8;
      font-size: 16px;
      pointer-events: none;
    }

    #dir-search-input {
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      padding: 12px 14px 12px 42px;
      font-size: 14px;
      color: #fff;
      font-family: inherit;
      outline: none;
      transition: all 0.2s ease;
    }

    #dir-search-input:focus {
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--accent-cyan);
      box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
    }

    .dir-filters {
      padding: 10px 24px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      background: rgba(13, 19, 33, 0.8);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .filter-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 5px 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .filter-chip:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #fff;
    }

    .filter-chip.active {
      background: rgba(6, 182, 212, 0.25);
      border-color: var(--accent-cyan);
      color: #38bdf8;
    }

    .dir-body {
      padding: 18px 24px;
      overflow-y: auto;
      max-height: calc(85vh - 220px);
      scrollbar-width: thin;
      scrollbar-color: rgba(56, 189, 248, 0.3) transparent;
    }

    .dir-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(265px, 1fr));
      gap: 12px;
    }

    .room-dir-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
    }

    .room-dir-card:hover {
      background: rgba(255, 255, 255, 0.07);
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-id-pill {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 13px;
      padding: 3px 8px;
      border-radius: 6px;
      color: #fff;
    }

    .card-floor-tag {
      font-size: 10px;
      font-weight: 700;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 7px;
      border-radius: 10px;
    }

    .card-title {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      line-height: 1.25;
    }

    .card-sub {
      font-size: 11px;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .card-actions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-top: 4px;
    }

    .btn-nav-travel {
      background: linear-gradient(135deg, #0284c7, #06b6d4);
      border: none;
      color: #fff;
      font-weight: 700;
      font-size: 11px;
      padding: 8px 6px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.2s ease;
      box-shadow: 0 3px 10px rgba(2, 132, 199, 0.3);
    }

    .btn-nav-travel:hover {
      background: linear-gradient(135deg, #0369a1, #0891b2);
      transform: translateY(-1px);
    }

    .btn-nav-teleport {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #e2e8f0;
      font-weight: 600;
      font-size: 11px;
      padding: 8px 6px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      transition: all 0.2s ease;
    }

    .btn-nav-teleport:hover {
      background: rgba(255, 255, 255, 0.16);
      color: #fff;
    }

    /* LIVE ROUTE FOLLOWER & HOLD-TO-FOLLOW HUD */
    .route-follower-hud {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(30px);
      background: rgba(13, 19, 33, 0.95);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 2px solid var(--accent-cyan);
      border-radius: 40px;
      padding: 10px 22px;
      display: flex;
      align-items: center;
      gap: 16px;
      z-index: 100;
      box-shadow: 0 16px 50px rgba(0, 0, 0, 0.85), 0 0 30px rgba(6, 182, 212, 0.4);
      opacity: 0;
      pointer-events: none;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }

    .route-follower-hud.active {
      opacity: 1;
      pointer-events: auto;
      transform: translateX(-50%) translateY(0);
    }

    .route-info-box {
      display: flex;
      flex-direction: column;
      gap: 2px;
      border-right: 1px solid rgba(255, 255, 255, 0.12);
      padding-right: 16px;
    }

    .route-dest-badge {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .route-dest-id {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 5px;
      color: #fff;
    }

    .route-dest-title {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
    }

    .route-dist-txt {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #38bdf8;
      font-weight: 600;
    }

    /* THE MAIN "HOLD TO FOLLOW LINE" BUTTON */
    .btn-hold-follow {
      background: linear-gradient(135deg, #0284c7, #06b6d4);
      border: none;
      color: #ffffff;
      padding: 12px 26px;
      border-radius: 28px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.04em;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 18px rgba(2, 132, 199, 0.5);
      transition: all 0.15s ease;
      user-select: none;
      touch-action: manipulation;
    }

    .btn-hold-follow:hover {
      background: linear-gradient(135deg, #0369a1, #0891b2);
      transform: scale(1.03);
    }

    .btn-hold-follow:active, .btn-hold-follow.pressing {
      background: linear-gradient(135deg, #10b981, #059669);
      box-shadow: 0 0 25px rgba(16, 185, 129, 0.8), inset 0 2px 6px rgba(0,0,0,0.3);
      transform: scale(0.97);
    }

    .follow-icon {
      font-size: 18px;
    }

    .follow-sub {
      font-size: 10px;
      opacity: 0.8;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
    }

    .btn-clear-route {
      background: rgba(244, 63, 94, 0.18);
      border: 1px solid rgba(244, 63, 94, 0.4);
      color: #fb7185;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-clear-route:hover {
      background: rgba(244, 63, 94, 0.4);
      color: #fff;
      transform: scale(1.1);
    }

    /* DIRECTORY CARD SINGLE "SET ROUTE" BUTTON */
    .btn-card-route {
      width: 100%;
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.25), rgba(6, 182, 212, 0.25));
      border: 1px solid rgba(56, 189, 248, 0.45);
      color: #38bdf8;
      font-weight: 700;
      font-size: 12px;
      padding: 9px 12px;
      border-radius: 9px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      margin-top: 4px;
    }

    .btn-card-route:hover {
      background: linear-gradient(135deg, #0284c7, #06b6d4);
      border-color: #38bdf8;
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(6, 182, 212, 0.35);
    }


    /* DRAWING TOOLBAR HUD */
    .draw-toolbar-hud {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: rgba(13, 19, 33, 0.96);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1.5px solid var(--accent-cyan);
      border-radius: 40px;
      padding: 8px 18px;
      display: flex;
      align-items: center;
      gap: 14px;
      z-index: 90;
      box-shadow: 0 15px 45px rgba(0, 0, 0, 0.8), 0 0 25px rgba(6, 182, 212, 0.35);
      opacity: 0;
      pointer-events: none;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }

    .draw-toolbar-hud.active {
      opacity: 1;
      pointer-events: auto;
      transform: translateX(-50%) translateY(0);
    }

    .draw-tag {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-right: 1px solid rgba(255, 255, 255, 0.12);
      padding-right: 12px;
    }

    .color-swatches {
      display: flex;
      align-items: center;
      gap: 6px;
      border-right: 1px solid rgba(255, 255, 255, 0.12);
      padding-right: 12px;
    }

    .color-swatch {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid transparent;
      transition: all 0.15s ease;
    }

    .color-swatch:hover {
      transform: scale(1.2);
    }

    .color-swatch.active {
      border-color: #fff;
      transform: scale(1.15);
      box-shadow: 0 0 10px currentColor;
    }

    .draw-dist-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      color: #e2e8f0;
      background: rgba(255, 255, 255, 0.08);
      padding: 4px 10px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .btn-draw-action {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #f8fafc;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
    }

    .btn-draw-action:hover {
      background: rgba(255, 255, 255, 0.18);
      transform: translateY(-1px);
    }

    .btn-draw-walk {
      background: linear-gradient(135deg, #10b981, #059669);
      border: none;
      color: #fff;
      box-shadow: 0 3px 12px rgba(16, 185, 129, 0.4);
    }

    .btn-draw-walk:hover {
      background: linear-gradient(135deg, #059669, #047857);
    }

    .btn-draw-walk:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }


    /* =========================================================================
       --- RESPONSIVE MOBILE STYLES & LAYOUT ---
       ========================================================================= */
    #mobile-menu-backdrop {
      display: none;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(4px);
      z-index: 40;
    }

    #mobile-menu-backdrop.open {
      display: block;
    }

    /* Floating Quick Bar for Mobile */
    .mobile-floating-bar {
      display: none;
      position: absolute;
      top: 12px;
      right: 12px;
      z-index: 50;
      gap: 6px;
    }

    .m-btn {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: var(--panel-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--panel-border);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
      touch-action: manipulation;
    }

    .m-btn.active {
      background: rgba(6, 182, 212, 0.3);
      border-color: var(--accent-cyan);
      color: #38bdf8;
    }

    /* VIRTUAL ANALOG JOYSTICK (FOR MOBILE TOUCH MOVEMENT) */
    .virtual-joystick-zone {
      display: none;
      position: absolute;
      bottom: 24px;
      left: 20px;
      width: 140px;
      height: 140px;
      z-index: 50;
      touch-action: none;
    }

    .joystick-base {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      background: rgba(13, 19, 33, 0.65);
      backdrop-filter: blur(10px);
      border: 2px solid rgba(56, 189, 248, 0.35);
      position: absolute;
      top: 10px;
      left: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }

    .joystick-stick {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0284c7, #06b6d4);
      border: 2px solid rgba(255, 255, 255, 0.4);
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.6);
      position: absolute;
      top: 34px;
      left: 34px;
      pointer-events: none;
      transition: transform 0.05s ease;
    }

    @media (max-width: 768px) {
      /* Show mobile controls */
      .mobile-floating-bar {
        display: flex;
      }

      .virtual-joystick-zone {
        display: block;
      }

      /* Hide desktop D-pad & Controls HUD on mobile */
      .virtual-dpad {
        display: none !important;
      }

      .controls-hud {
        display: none !important;
      }

      /* Compact top bar */
      .top-bar {
        top: 10px;
        left: 10px;
        right: 10px;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        pointer-events: none;
      }

      .brand-card {
        padding: 6px 12px;
        border-radius: 10px;
        gap: 8px;
        pointer-events: auto;
      }

      .brand-logo {
        width: 28px;
        height: 28px;
        font-size: 18px;
        border-radius: 7px;
      }

      .brand-info h1 {
        font-size: 13px;
      }

      .brand-info p {
        display: none; /* Hide subtitle to keep header compact */
      }

      .location-hud {
        padding: 5px 14px;
        font-size: 11px;
        border-radius: 20px;
        gap: 6px;
      }

      .loc-text {
        font-size: 11px;
        max-width: 180px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .loc-floor {
        font-size: 9px;
        padding: 2px 6px;
      }

      /* Hide desktop top-actions on mobile */
      .top-actions {
        display: none !important;
      }

      /* Minimap becomes collapsible floating radar */
      .minimap-container {
        display: none;
        top: 60px;
        right: 12px;
        width: 170px;
        height: 120px;
        border-radius: 12px;
        z-index: 45;
      }

      .minimap-container.mobile-open {
        display: flex;
      }

      /* Left Dock becomes off-canvas drawer */
      .left-dock {
        top: 0;
        left: 0;
        bottom: 0;
        height: 100%;
        max-height: 100%;
        width: 280px;
        background: rgba(10, 15, 28, 0.98);
        border-right: 1px solid var(--panel-border);
        border-radius: 0 16px 16px 0;
        transform: translateX(-100%);
        transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 45;
        padding: 20px 16px 60px;
      }

      .left-dock.mobile-open {
        transform: translateX(0);
      }

      .dock-panel {
        width: 100%;
      }

      /* Route Follower HUD on Mobile */
      .route-follower-hud {
        width: 92%;
        max-width: 420px;
        bottom: 14px;
        padding: 8px 14px;
        gap: 10px;
      }

      .route-info-box {
        padding-right: 10px;
      }

      .route-dest-title {
        font-size: 12px;
        max-width: 120px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .btn-hold-follow {
        padding: 10px 16px;
        font-size: 11px;
        border-radius: 20px;
        gap: 6px;
      }

      .follow-sub {
        display: none;
      }

      /* Directory Modal Mobile Fullscreen Bottom Sheet */
      .directory-modal-backdrop {
        align-items: flex-end;
      }

      .directory-modal {
        width: 100%;
        max-width: 100%;
        max-height: 88vh;
        border-radius: 24px 24px 0 0;
        border-bottom: none;
      }

      .dir-header {
        padding: 14px 18px 10px;
      }

      .dir-title-area h2 {
        font-size: 16px;
      }

      .dir-title-area p {
        font-size: 10px;
      }

      .dir-search-bar {
        padding: 10px 18px;
      }

      #dir-search-input {
        padding: 10px 12px 10px 36px;
        font-size: 13px;
      }

      .dir-filters {
        padding: 8px 18px;
        overflow-x: auto;
        flex-wrap: nowrap;
        scrollbar-width: none;
      }

      .dir-filters::-webkit-scrollbar {
        display: none;
      }

      .filter-chip {
        white-space: nowrap;
        flex-shrink: 0;
      }

      .dir-body {
        padding: 12px 16px 40px;
      }

      .dir-grid {
        grid-template-columns: 1fr;
      }

      /* Room Detail Drawer on Mobile */
      .right-drawer {
        top: auto;
        bottom: 0;
        right: 0;
        left: 0;
        width: 100%;
        border-radius: 20px 20px 0 0;
        max-height: 70vh;
        overflow-y: auto;
      }

      /* Drawing Toolbar on Mobile */
      .draw-toolbar-hud {
        width: 94%;
        bottom: 12px;
        padding: 6px 12px;
        gap: 8px;
        overflow-x: auto;
      }

      .draw-tag {
        font-size: 10px;
        padding-right: 8px;
      }

      .color-swatch {
        width: 18px;
        height: 18px;
      }

      .draw-dist-badge {
        font-size: 10px;
        padding: 3px 6px;
      }

      .btn-draw-action {
        padding: 5px 8px;
        font-size: 10px;
      }
    }

  </style>

  <!-- Local libraries with CDN fallback -->
  <script src="lib/three.min.js"></script>
  <script src="lib/OrbitControls.js"></script>
  <script src="lib/GLTFExporter.js"></script>
  <script src="lib/OBJExporter.js"></script>
</head>
<body>

  <div id="webgl-container"></div>

  <!-- TOP HEADER -->
  <div class="top-bar">
    <div class="brand-card">
      <div class="brand-logo">+</div>
      <div class="brand-info">
        <h1>City General Hospital</h1>
        <p>3D High-Fidelity Twin • 2 Stacked Floors</p>
      </div>
    </div>

    <!-- CURRENT LOCATION BANNER -->
    <div class="location-hud" id="loc-banner">
      <span class="loc-icon">📍</span>
      <span class="loc-floor" id="hud-floor">FLOOR 1</span>
      <span class="loc-text" id="hud-room">Main Entrance Lobby</span>
    </div>

    <!-- TOP RIGHT BUTTONS -->
    <div class="top-actions">
      <button class="btn-action active" id="btn-open-directory" style="background: linear-gradient(135deg, #0284c7, #06b6d4); border:none; box-shadow:0 3px 12px rgba(6,182,212,0.35);">
        <span>🔍</span> Search & Directory (All Rooms)
      </button>
      <button class="btn-action btn-primary" id="btn-toggle-mode">
        <span>🎮</span> Game Walkthrough Mode
      </button>
      <button class="btn-action" id="btn-toggle-draw">
        <span>✏️</span> Draw Line / Route
      </button>
      <button class="btn-action" id="btn-view-toggle">
        <span>👁️</span> 3rd Person
      </button>
      <button class="btn-action" id="btn-labels-toggle">
        <span>🏷️</span> Wall Labels: OFF
      </button>
      <button class="btn-action" id="btn-sound-toggle">
        <span>🔊</span> Sound: On
      </button>
    </div>
  </div>

  <!-- MINIMAP RADAR IN TOP RIGHT -->
  <div class="minimap-container">
    <div class="minimap-header">
      <span>MINIMAP (<strong id="mini-floor-txt">Floor 1</strong>)</span>
      <span style="font-size:9px; color:#38bdf8;">GPS RADAR</span>
    </div>
    <canvas id="minimap-canvas" width="250" height="150"></canvas>
  </div>

  <!-- INTERACTION PROMPT -->
  <div class="interaction-prompt" id="interact-prompt">
    Press <span class="key-badge">E</span> to Take Elevator
  </div>

  <!-- ELEVATOR MODAL -->
  <div class="elevator-modal" id="elevator-modal">
    <h2>Hospital Elevator Core</h2>
    <p>Select target destination floor:</p>
    <div class="elevator-buttons">
      <div class="elev-floor-btn current" id="elev-btn-f1">
        <span class="elev-num">1</span>
        <span class="elev-sub">Ground Floor<br>(Emergency, OPD, Cafeteria)</span>
      </div>
      <div class="elev-floor-btn" id="elev-btn-f2">
        <span class="elev-num">2</span>
        <span class="elev-sub">Upper Floor<br>(ICU, Surgery, Maternity)</span>
      </div>
    </div>
    <button class="btn-action" style="margin: 16px auto 0; width: 100px; justify-content: center;" id="elev-close-btn">Close</button>
  </div>

  <!-- LEFT DOCK -->
  <div class="left-dock">
    <div class="dock-panel">
      <h3>Exploration Mode</h3>
      <div class="pill-group">
        <button class="pill-btn active" id="btn-mode-game">
          <span class="pill-icon">🚶</span> Walkable Doctor
        </button>
        <button class="pill-btn" id="btn-mode-orbit">
          <span class="pill-icon">🌐</span> Orbit Overview (Free)
        </button>
      </div>
    </div>

    <div class="dock-panel">
      <h3>Floor View & Cutaway</h3>
      <div class="pill-group">
        <button class="pill-btn active" id="btn-floor-active">
          <span class="pill-icon">🏢</span> Active Floor
        </button>
        <button class="pill-btn" id="btn-floor-both">
          <span class="pill-icon">🏬</span> Both Floors Stacked
        </button>
        <button class="pill-btn" id="btn-floor-f1">
          <span class="pill-icon">①</span> Floor 1 Only
        </button>
        <button class="pill-btn" id="btn-floor-f2">
          <span class="pill-icon">②</span> Floor 2 Only
        </button>
      </div>
    </div>

    <div class="dock-panel">
      <h3>Wall Labels & Visuals</h3>
      <div class="pill-group">
        <button class="pill-btn" id="btn-dock-labels">
          <span class="pill-icon">🏷️</span> Colored Wall Signs: Off
        </button>
        <button class="pill-btn" id="btn-dock-cam-dist">
          <span class="pill-icon">🎥</span> Cam Distance: Medium
        </button>
      </div>
    </div>

    <div class="dock-panel">
      <h3>Teleport to Department</h3>
      <div class="pill-group">
        <button class="pill-btn" data-teleport="101">🚨 Emergency (F1)</button>
        <button class="pill-btn" data-teleport="111">🧪 Isolation Room (F1)</button>
        <button class="pill-btn" data-teleport="110">🛏️ General Ward (F1)</button>
        <button class="pill-btn" data-teleport="109">🛏️ General Ward Left (F1)</button>
        <button class="pill-btn" data-teleport="108">❤️ Cardiology (F1)</button>
        <button class="pill-btn" data-teleport="102">🛎️ Reception (F1)</button>
        <button class="pill-btn" data-teleport="113">☕ Cafeteria (F1)</button>
        <button class="pill-btn" data-teleport="201">🫀 ICU (F2)</button>
        <button class="pill-btn" data-teleport="203">🔬 Operation Theatre (F2)</button>
        <button class="pill-btn" data-teleport="206">👶 Maternity Ward (F2)</button>
        <button class="pill-btn" data-teleport="210">🧸 Pediatrics Ward (F2)</button>
        <button class="pill-btn" data-teleport="212">💼 Conference (F2)</button>
      </div>
    </div>
  </div>

  <!-- RIGHT ROOM DETAIL DRAWER -->
  <div class="right-drawer" id="room-drawer">
    <div class="drawer-header">
      <span class="room-badge" id="d-badge">ROOM 101</span>
      <button class="close-btn" id="close-drawer">✕</button>
    </div>
    <h2 class="room-title" id="d-title">Emergency Room</h2>
    <div class="room-category">
      <span class="dot-indicator" id="d-dot" style="background:#ef4444;"></span>
      <span id="d-cat">Emergency / Trauma</span>
    </div>

    <div class="detail-grid">
      <div class="detail-card">
        <div class="label">Floor Level</div>
        <div class="val" id="d-floor">1st Floor</div>
      </div>
      <div class="detail-card">
        <div class="label">Dimensions</div>
        <div class="val" id="d-size">7m × 6m (42m²)</div>
      </div>
      <div class="detail-card">
        <div class="label">Capacity</div>
        <div class="val" id="d-beds">2 Trauma Beds</div>
      </div>
      <div class="detail-card">
        <div class="label">Status</div>
        <div class="val" style="color:#10b981;" id="d-status">Active 24/7</div>
      </div>
    </div>

    <div class="equipment-list">
      <h4>Clinical Equipment & Features</h4>
      <div id="d-equipment">
        • Crash Carts with Defibrillator<br>
        • High-acuity Vitals Patient Monitors<br>
        • Oxygen & Suction Medical Gas Ports
      </div>
    </div>
  </div>

  <!-- ON-SCREEN VIRTUAL DPAD -->
  <div class="virtual-dpad">
    <div></div>
    <button class="dpad-btn" id="btn-dpad-up">▲</button>
    <div></div>
    <button class="dpad-btn" id="btn-dpad-left">◀</button>
    <button class="dpad-btn" id="btn-dpad-action">E</button>
    <button class="dpad-btn" id="btn-dpad-right">▶</button>
    <div></div>
    <button class="dpad-btn" id="btn-dpad-down">▼</button>
    <div></div>
  </div>

  <!-- BOTTOM CONTROLS HUD -->
  <div class="controls-hud">
    <span><span class="key-badge">W</span><span class="key-badge">A</span><span class="key-badge">S</span><span class="key-badge">D</span> Move</span>
    <span><span class="key-badge">Shift</span> Sprint</span>
    <span><span class="key-badge">Mouse Drag</span> Look Around</span>
    <span><span class="key-badge">V</span> 1st/3rd View</span>
    <span><span class="key-badge">L</span> Wall Labels</span>
    <span><span class="key-badge">E</span> Elevator</span>
  </div>

  <script>
    // Canvas roundRect Polyfill for mobile browsers
    if (typeof CanvasRenderingContext2D !== "undefined" && !CanvasRenderingContext2D.prototype.roundRect) {
      CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
        if (!r) r = 0;
        const radius = typeof r === "number" ? { tl: r, tr: r, br: r, bl: r } : r;
        this.beginPath();
        this.moveTo(x + (radius.tl || 0), y);
        this.lineTo(x + w - (radius.tr || 0), y);
        this.quadraticCurveTo(x + w, y, x + w, y + (radius.tr || 0));
        this.lineTo(x + w, y + h - (radius.br || 0));
        this.quadraticCurveTo(x + w, y + h, x + w - (radius.br || 0), y + h);
        this.lineTo(x + (radius.bl || 0), y + h);
        this.quadraticCurveTo(x, y + h, x, y + h - (radius.bl || 0));
        this.lineTo(x, y + (radius.tl || 0));
        this.quadraticCurveTo(x, y, x + (radius.tl || 0), y);
        this.closePath();
        return this;
      };
    }

    // --- 1. PROCEDURAL TEXTURES (REALISTIC PBR GRAPHICS) ---
    function createPolishedFloorTexture() {
      const canvas = document.createElement("canvas");
      canvas.width = 512;
      canvas.height = 512;
      const ctx = canvas.getContext("2d");

      // Polished hospital linoleum terrazzo base
      ctx.fillStyle = "#f8fafc";
      ctx.fillRect(0, 0, 512, 512);

      // Subtle fine speckling
      for (let i = 0; i < 1500; i++) {
        const x = Math.random() * 512;
        const y = Math.random() * 512;
        const r = Math.random() * 1.5;
        const shade = Math.random() > 0.5 ? "rgba(203, 213, 225, 0.35)" : "rgba(148, 163, 184, 0.25)";
        ctx.fillStyle = shade;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }

      // Elegant architectural tile joint seams (64px grid)
      ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
      ctx.lineWidth = 1.5;
      for (let x = 0; x <= 512; x += 64) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, 512);
        ctx.stroke();
      }
      for (let y = 0; y <= 512; y += 64) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(512, y);
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(canvas);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(5, 5);
      return tex;
    }

    function createWallStuccoTexture() {
      const canvas = document.createElement("canvas");
      canvas.width = 256;
      canvas.height = 256;
      const ctx = canvas.getContext("2d");

      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, 256, 256);

      // Very subtle plaster grain
      for (let i = 0; i < 3000; i++) {
        const x = Math.random() * 256;
        const y = Math.random() * 256;
        ctx.fillStyle = Math.random() > 0.5 ? "rgba(0, 0, 0, 0.02)" : "rgba(255, 255, 255, 0.03)";
        ctx.fillRect(x, y, 1, 1);
      }

      const tex = new THREE.CanvasTexture(canvas);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(8, 4);
      return tex;
    }

    const corridorTileTex = createPolishedFloorTexture();
    const wallStuccoTex = createWallStuccoTexture();

    // --- 2. MATERIALS & COLOR PALETTES ---
    // Realistic Polished Hospital Vinyl Floor Material
    const floorSlabMat = new THREE.MeshStandardMaterial({
      color: 0xf8fafc,
      roughness: 0.18, // Polished hospital shine
      metalness: 0.08,
      map: corridorTileTex
    });

    const baseboardMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b, // Dark charcoal kickplate
      roughness: 0.35,
      metalness: 0.2
    });

    const bumperRailMat = new THREE.MeshStandardMaterial({
      color: 0x0284c7, // Hospital blue crash guard
      roughness: 0.3,
      metalness: 0.15
    });

    const stainlessMat = new THREE.MeshStandardMaterial({
      color: 0xe2e8f0,
      roughness: 0.2,
      metalness: 0.85
    });

    const glassMat = new THREE.MeshPhysicalMaterial({
      color: 0xbae6fd,
      transmission: 0.85,
      transparent: true,
      opacity: 0.55,
      roughness: 0.08,
      ior: 1.5
    });

    const ceilingPanelMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      emissive: 0xffffff,
      emissiveIntensity: 0.75,
      roughness: 0.3
    });

    // Department Category Colors (Distinct, professional healthcare color scheme)
    const CAT_COLORS = {
      "Emergency": { hex: 0xef4444, css: "#ef4444", text: "#ffffff", border: "#b91c1c" },
      "Diagnostics": { hex: 0x0284c7, css: "#0284c7", text: "#ffffff", border: "#0369a1" },
      "Wards": { hex: 0x10b981, css: "#10b981", text: "#ffffff", border: "#047857" },
      "Surgical": { hex: 0x0d9488, css: "#0d9488", text: "#ffffff", border: "#0f766e" },
      "Offices": { hex: 0x6366f1, css: "#6366f1", text: "#ffffff", border: "#4338ca" },
      "Facilities": { hex: 0xf59e0b, css: "#f59e0b", text: "#ffffff", border: "#b45309" }
    };

    // --- 3. DIMENSIONS & ROOM DATA ---
    const FLOOR_HEIGHT = 3.6; // Floor 2 sits exactly at Y = 3.6m directly atop Floor 1
    const WALL_HEIGHT = 2.8;

    const ROOM_DATA = [
      // FIRST FLOOR (Ground Floor, 40m x 25m)
      { id: "101", name: "Emergency Room", floor: 1, x: 0, z: 19, w: 7, d: 6, color: 0xef4444, cat: "Emergency", beds: "2 Trauma Beds", eq: "Emergency trauma stretchers, crash cart, vitals monitoring, oxygen hookup, rapid response station" },
      { id: "102", name: "Reception", floor: 1, x: 7, z: 19, w: 6, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "3 Check-in Desks", eq: "Admissions computers, visitor badge printers, patient queue ticketing, intercom" },
      { id: "103", name: "OPD Consultation", floor: 1, x: 13, z: 19, w: 6, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "1 Exam Table", eq: "Outpatient doctor workstation, examination couch, blood pressure unit, diagnostic otoscope" },
      { id: "104", name: "Pharmacy", floor: 1, x: 19, z: 19, w: 5, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "Dispensing Hub", eq: "Automated pill dispensing carousel, refrigerated drug lockers, point-of-sale systems" },
      { id: "105", name: "Laboratory", floor: 1, x: 24, z: 19, w: 5, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "Diagnostic Lab", eq: "Centrifuges, automated blood analyzers, optical microscopes, fume hood, incubator" },
      { id: "106", name: "Radiology", floor: 1, x: 29, z: 19, w: 5.5, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "1 CT / X-Ray Gantry", eq: "Full multi-slice CT/X-Ray ring scanner, motorized sliding table, lead-lined control console" },
      { id: "107", name: "Ultrasound", floor: 1, x: 34.5, z: 19, w: 5.5, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "1 Ultrasound Table", eq: "Doppler ultrasound console, cardiac & abdominal probes, high-resolution diagnosis display" },
      
      { id: "108", name: "Cardiology", floor: 1, x: 0, z: 12.5, w: 11, d: 4.5, color: 0x6366f1, cat: "Offices", beds: "1 ECG / Stress Unit", eq: "Electrocardiogram (ECG) cart, stress treadmill, echocardiography station, cardiologist desk" },
      { id: "109", name: "General Ward", floor: 1, x: 0, z: 8, w: 11, d: 4.5, color: 0x10b981, cat: "Wards", beds: "4 Inpatient Beds", eq: "Adjustable hospital beds, IV infusion stands, privacy dividing curtains, nurse call buttons" },
      
      { id: "110", name: "General Ward", floor: 1, x: 29, z: 12.5, w: 11, d: 4.5, color: 0x10b981, cat: "Wards", beds: "4 Inpatient Beds", eq: "Multi-patient general recovery ward beds with personal lockers, reading lamps, overbed tables" },
      { id: "111", name: "Isolation Room", floor: 1, x: 29, z: 8, w: 11, d: 4.5, color: 0x059669, cat: "Wards", beds: "1 Isolated Bed", eq: "Negative-pressure ventilation system, airtight ante-room, dedicated sanitization station" },
      
      { id: "112", name: "Restroom", floor: 1, x: 0, z: 0, w: 7, d: 6, color: 0x64748b, cat: "Facilities", beds: "Public Facilities", eq: "Wheelchair accessible cubicles, sensor taps, automatic hand dryers, baby changing table" },
      { id: "113", name: "Cafeteria", floor: 1, x: 7, z: 0, w: 10, d: 6, color: 0xf59e0b, cat: "Facilities", beds: "40 Seats", eq: "Hot food service buffet counters, dining tables, beverage coolers, coffee station" },
      { id: "114", name: "Waiting Area", floor: 1, x: 17, z: 0, w: 6, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "Main Entrance", eq: "Double automatic sliding doors, triage waiting chairs, informational display monitor" },
      { id: "115", name: "Information Desk", floor: 1, x: 23, z: 0, w: 6, d: 6, color: 0x0284c7, cat: "Diagnostics", beds: "Concierge Station", eq: "Main lobby help desk, facility directory screens, patient navigation support" },
      { id: "116", name: "Administration", floor: 1, x: 29, z: 0, w: 11, d: 6, color: 0x0d9488, cat: "Offices", beds: "6 Workstations", eq: "Executive hospital management desks, financial billing files, secure record storage" },
      
      { id: "Lobby-1", name: "Lobby (First Floor)", floor: 1, x: 17.5, z: 8, w: 8.5, d: 9, color: 0xf1f5f9, cat: "Diagnostics", beds: "Main Lobby", eq: "Central open circulation atrium, rows of cushioned waiting chairs, indoor ornamental planters" },
      { id: "Stairs-1", name: "Stairs (To 2nd Floor)", floor: 1, x: 13, z: 8, w: 4.5, d: 8.5, color: 0x475569, cat: "Facilities", beds: "Stairwell", eq: "Wide fire-rated concrete stairs with dual stainless steel grab handrails, connecting to Floor 2" },
      { id: "Elevator-1", name: "Elevator", floor: 1, x: 22.5, z: 9.5, w: 3.0, d: 6.0, color: 0x334155, cat: "Facilities", beds: "Dual Elevator", eq: "High-speed hospital gurney size elevator connecting to Floor 2" },

      // SECOND FLOOR (Upper Floor, 40m x 25m)
      { id: "201", name: "ICU", floor: 2, x: 0, z: 19, w: 7, d: 6, color: 0xef4444, cat: "Surgical", beds: "2 ICU Beds", eq: "Advanced hemodynamic monitors, invasive ventilators, syringe infusion pumps, defibrillator" },
      { id: "202", name: "ICU Support", floor: 2, x: 7, z: 19, w: 5, d: 6, color: 0x0284c7, cat: "Surgical", beds: "Nurse Station", eq: "Central telemetry monitoring station, emergency crash cart, sterile medication trolley" },
      { id: "203", name: "Operation Theatre 1", floor: 2, x: 12, z: 19, w: 7, d: 6, color: 0x0d9488, cat: "Surgical", beds: "1 Surgical Suite", eq: "Hydraulic surgical table, dual ceiling shadowless lamps, anesthesia delivery station, laparoscopic tower" },
      { id: "204", name: "Operation Theatre 2", floor: 2, x: 19, z: 19, w: 7, d: 6, color: 0x0d9488, cat: "Surgical", beds: "1 Surgical Suite", eq: "General surgery operating suite, surgical suction unit, electrosurgical generator, sterile back-tables" },
      { id: "205", name: "Sterilization", floor: 2, x: 26, z: 19, w: 6, d: 6, color: 0x0284c7, cat: "Surgical", beds: "CSSD Hub", eq: "High-capacity steam autoclaves, ultrasonic instrument washer, surgical packaging counter" },
      { id: "206", name: "Maternity Ward", floor: 2, x: 32, z: 19, w: 8, d: 6, color: 0xf472b6, cat: "Wards", beds: "3 Maternity Beds", eq: "Specialized birthing beds, infant warming incubators, fetal doppler monitors, nursing chairs" },

      { id: "207", name: "Doctors' Offices", floor: 2, x: 0, z: 14, w: 11, d: 3, color: 0x6366f1, cat: "Offices", beds: "Chief Physician", eq: "Executive desk, medical literature library, diagnostic viewing light box, patient meeting sofa" },
      { id: "208", name: "Doctors' Offices", floor: 2, x: 0, z: 11, w: 11, d: 3, color: 0x6366f1, cat: "Offices", beds: "Physician Suite", eq: "Specialist consultation workstation, electronic medical records PC, examination couch" },
      { id: "209", name: "Doctors' Offices", floor: 2, x: 0, z: 8, w: 11, d: 3, color: 0x6366f1, cat: "Offices", beds: "Physician Suite", eq: "Doctor consultation desk, computer, visitor seating, anatomical wall charts" },

      { id: "210", name: "Pediatrics Ward", floor: 2, x: 29, z: 12.5, w: 11, d: 4.5, color: 0x10b981, cat: "Wards", beds: "3 Child Beds", eq: "Colorful pediatric beds, child safety rails, interactive activity play table, child-friendly murals" },
      { id: "211", name: "Pediatrics Ward", floor: 2, x: 29, z: 8, w: 11, d: 4.5, color: 0x10b981, cat: "Wards", beds: "3 Infant Beds", eq: "Infant cribs and junior beds, comfortable recliner chairs for parents, baby changing table" },

      { id: "212", name: "Conference Room", floor: 2, x: 0, z: 0, w: 9, d: 6, color: 0xf59e0b, cat: "Facilities", beds: "16 Board Seats", eq: "16-seat conference boardroom table, executive leather chairs, 4K teleconference screen" },
      { id: "213", name: "Training Room", floor: 2, x: 9, z: 0, w: 7, d: 6, color: 0xf59e0b, cat: "Facilities", beds: "24 Seats", eq: "Tiered seminar training tables, lecturer presentation podium, ceiling mounted projector" },
      { id: "214", name: "Pantry", floor: 2, x: 16, z: 0, w: 6, d: 6, color: 0x0284c7, cat: "Facilities", beds: "Staff Kitchen", eq: "Kitchen cabinets, microwave oven, full-size refrigerator, espresso machine, dining counter" },
      { id: "215", name: "Restroom", floor: 2, x: 22, z: 0, w: 6, d: 6, color: 0x64748b, cat: "Facilities", beds: "Staff Restroom", eq: "Individual restroom cubicles, wash hand basins, touchless soap and towel dispensers" },
      { id: "216", name: "Staff Lounge", floor: 2, x: 28, z: 0, w: 12, d: 6, color: 0x0d9488, cat: "Facilities", beds: "Relaxation Lounge", eq: "Plush sectional sofas, coffee tables, soft ambient lighting, lockers, smart TV" },

      { id: "Lobby-2", name: "Lobby (Second Floor)", floor: 2, x: 17.5, z: 8, w: 8.5, d: 9, color: 0xf1f5f9, cat: "Diagnostics", beds: "2nd Floor Lobby", eq: "Upper atrium hallway, waiting seats, safety glass balustrade overlooking center, decorative plants" },
      { id: "Stairs-2", name: "Stairs (To 1st Floor)", floor: 2, x: 13, z: 8, w: 4.5, d: 8.5, color: 0x475569, cat: "Facilities", beds: "Upper Stairwell", eq: "Upper floor stair landing with fire exit push bars, connecting to Floor 1" },
      { id: "Elevator-2", name: "Elevator", floor: 2, x: 22.5, z: 9.5, w: 3.0, d: 6.0, color: 0x334155, cat: "Facilities", beds: "Upper Elevator", eq: "Second floor elevator lobby call panel and illuminated direction arrows" },
    ];

    // --- 4. AUDIO SYSTEM ---
    class HospitalSoundSystem {
      constructor() {
        this.ctx = null;
        this.enabled = true;
      }
      init() {
        if (!this.ctx) {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) this.ctx = new AudioContext();
        }
      }
      playFootstep() {
        if (!this.enabled || !this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(75, now);
        osc.frequency.exponentialRampToValueAtTime(25, now + 0.08);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.08);
      }
      playElevatorChime() {
        if (!this.enabled || !this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(587.33, now);
        osc.frequency.setValueAtTime(880.00, now + 0.15);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 1.2);
      }
      playRoomDing() {
        if (!this.enabled || !this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(523.25, now);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.4);
      }
    }
    const sound = new HospitalSoundSystem();

    // --- 5. THREE.JS INITIALIZATION ---
    let scene, camera, renderer, controls;
    let floor1Group, floor2Group, groundGroup, stairsMeshGroup, elevatorCabin, labelsGroup;
    let roomMeshes = [];
    let wallColliders = [];
    let allWallMeshes = []; // Stored for raycast occlusion and dynamic transparency
    let occludedWallMeshes = new Set();

    let player;
    let playerPos = new THREE.Vector3(20, 0, 2); // Start at Main Entrance
    let playerRotY = Math.PI;
    let isGameMode = true;
    let isFirstPerson = false;
    let currentFloor = 1;
    let currentRoomId = "114";
    let elevatorMoving = false;
    let viewFilter = "active"; // "active", "both", "f1", "f2"
    let labelsVisible = false;
    let camDistanceSetting = 3.6; // 3.6m default distance (customizable)

    const keys = { w: false, a: false, s: false, d: false, shift: false };
    let mouseDrag = false;
    let prevMouseX = 0, prevMouseY = 0;
    let cameraPitch = 0.22;
    let currentCameraDistance = 3.6;

    const container = document.getElementById("webgl-container");
    const raycaster = new THREE.Raycaster();


    // =========================================================================
    // --- 22. INTERACTIVE 3D FLOOR LINE DRAWING SYSTEM ---
    // =========================================================================
    let isDrawMode = false;
    let isDrawingMouseActive = false;
    let drawnWaypoints = [];
    let drawnLineColor = 0x06b6d4;
    let drawnLineMeshGroup = new THREE.Group();
    let floorDrawPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    let drawRaycaster = new THREE.Raycaster();
    let mouseNDC = new THREE.Vector2();
    let drawCursorRing = null;

    function initDrawingSystem() {
      scene.add(drawnLineMeshGroup);

      // Interactive Pen Reticle cursor that sits on the floor
      const ringGeo = new THREE.RingGeometry(0.2, 0.3, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x06b6d4,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.85
      });
      drawCursorRing = new THREE.Mesh(ringGeo, ringMat);
      drawCursorRing.rotation.x = -Math.PI / 2;
      drawCursorRing.visible = false;
      scene.add(drawCursorRing);
    }

    function toggleDrawingMode(forcedState) {
      isDrawMode = (forcedState !== undefined) ? forcedState : !isDrawMode;
      const btn = document.getElementById("btn-toggle-draw");
      const toolbar = document.getElementById("draw-toolbar-hud");

      if (isDrawMode) {
        btn.classList.add("active");
        btn.innerHTML = `<span>✏️</span> Drawing: ON`;
        toolbar.classList.add("active");
        drawCursorRing.visible = true;
        // Hide controls hud temporarily while drawing
        document.querySelector(".controls-hud").style.display = "none";
      } else {
        btn.classList.remove("active");
        btn.innerHTML = `<span>✏️</span> Draw Line / Route`;
        toolbar.classList.remove("active");
        drawCursorRing.visible = false;
        isDrawingMouseActive = false;
        document.querySelector(".controls-hud").style.display = "flex";
      }
    }

    function getFloorIntersection(clientX, clientY) {
      const rect = renderer.domElement.getBoundingClientRect();
      mouseNDC.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      mouseNDC.y = -((clientY - rect.top) / rect.height) * 2 + 1;

      drawRaycaster.setFromCamera(mouseNDC, camera);

      // Floor height based on current floor
      const curFloorY = (currentFloor - 1) * FLOOR_HEIGHT;
      floorDrawPlane.set(new THREE.Vector3(0, 1, 0), -curFloorY);

      const hit = new THREE.Vector3();
      const intersected = drawRaycaster.ray.intersectPlane(floorDrawPlane, hit);

      if (intersected) {
        // Clamp to hospital bounds (X: 0 to 40, Z: 0 to 25)
        hit.x = Math.max(0.5, Math.min(39.5, hit.x));
        hit.z = Math.max(0.5, Math.min(24.5, hit.z));
        hit.y = curFloorY + 0.05; // Slightly elevated above floor
        return hit;
      }
      return null;
    }

    function addDrawnPoint(point) {
      if (!point) return;

      // Avoid adding points too close to previous point (< 0.35m)
      if (drawnWaypoints.length > 0) {
        const last = drawnWaypoints[drawnWaypoints.length - 1];
        if (last.distanceTo(point) < 0.35) return;
      }

      drawnWaypoints.push(point.clone());
      updateDrawnLineVisualization();
    }

    function updateDrawnLineVisualization() {
      // Clear previous lines
      while (drawnLineMeshGroup.children.length > 0) {
        drawnLineMeshGroup.remove(drawnLineMeshGroup.children[0]);
      }

      const walkBtn = document.getElementById("btn-walk-drawn-path");
      const distTxt = document.getElementById("draw-dist-txt");

      if (drawnWaypoints.length < 2) {
        walkBtn.disabled = true;
        distTxt.textContent = "Length: 0.0m";
        return;
      }

      walkBtn.disabled = false;

      // 1. Calculate path length
      let totalDist = 0;
      for (let i = 1; i < drawnWaypoints.length; i++) {
        totalDist += drawnWaypoints[i - 1].distanceTo(drawnWaypoints[i]);
      }
      distTxt.textContent = `Length: ${totalDist.toFixed(1)}m`;

      // 2. Draw glowing floor line
      const lineGeo = new THREE.BufferGeometry().setFromPoints(drawnWaypoints);
      const lineMat = new THREE.LineBasicMaterial({
        color: drawnLineColor,
        linewidth: 5,
        transparent: true,
        opacity: 0.95
      });
      const line = new THREE.Line(lineGeo, lineMat);
      drawnLineMeshGroup.add(line);

      // 3. Waypoint breadcrumb nodes
      const nodeMat = new THREE.MeshBasicMaterial({ color: drawnLineColor });
      for (let i = 0; i < drawnWaypoints.length; i++) {
        const pt = drawnWaypoints[i];
        const isStart = i === 0;
        const isEnd = i === drawnWaypoints.length - 1;

        const size = (isStart || isEnd) ? 0.28 : 0.12;
        const node = new THREE.Mesh(
          new THREE.CylinderGeometry(size, size, 0.04, 16),
          isStart ? new THREE.MeshBasicMaterial({ color: 0x10b981 }) : (isEnd ? new THREE.MeshBasicMaterial({ color: 0xf43f5e }) : nodeMat)
        );
        node.position.copy(pt);
        drawnLineMeshGroup.add(node);
      }
    }

    function undoLastDrawnPoint() {
      if (drawnWaypoints.length > 0) {
        drawnWaypoints.pop();
        updateDrawnLineVisualization();
      }
    }

    function clearDrawnLine() {
      drawnWaypoints = [];
      updateDrawnLineVisualization();
    }

    // AUTONOMOUSLY WALK THE USER-DRAWN PATH
    function walkDrawnPath() {
      if (drawnWaypoints.length < 2) return;

      // Copy waypoints for autonomous walk
      currentNavPath = drawnWaypoints.map(p => p.clone());
      currentNavIndex = 0;
      currentNavTargetRoom = { id: "Custom", name: "Drawn Custom Route", floor: currentFloor };
      isAutoNavigating = true;

      // Close draw mode and open active nav HUD
      toggleDrawingMode(false);
      const hud = document.getElementById("nav-active-hud");
      document.getElementById("nav-target-name").textContent = `Custom Drawn Line Route`;
      document.getElementById("nav-target-dist").textContent = `Walking along custom user-drawn path...`;
      hud.classList.add("active");
      sound.playElevatorChime();
    }


    // =========================================================================
    // --- 23. MOBILE TOUCH CONTROLS (JOYSTICK, TOUCH LOOK & PINCH ZOOM) ---
    // =========================================================================
    let touchJoystickActive = false;
    let joystickOriginX = 0, joystickOriginY = 0;
    let joystickVector = new THREE.Vector2(0, 0);
    let touchLookActive = false;
    let prevTouchLookX = 0, prevTouchLookY = 0;
    let touchLookId = null;
    let touchJoystickId = null;
    let initialPinchDistance = null;

    function initMobileControls() {
      const joystickZone = document.getElementById("joystick-zone");
      const joystickStick = document.getElementById("joystick-stick");
      const joystickBase = document.getElementById("joystick-base");

      // Mobile top floating action buttons
      document.getElementById("m-btn-search").addEventListener("click", () => openDirectoryModal());
      document.getElementById("m-btn-view").addEventListener("click", () => toggleCameraView());
      document.getElementById("m-btn-labels").addEventListener("click", () => toggleWallLabels());

      // Toggle Mobile Minimap
      document.getElementById("m-btn-map").addEventListener("click", function() {
        const mini = document.querySelector(".minimap-container");
        mini.classList.toggle("mobile-open");
        this.classList.toggle("active", mini.classList.contains("mobile-open"));
      });

      // Toggle Mobile Menu Drawer
      const menuBackdrop = document.getElementById("mobile-menu-backdrop");
      const leftDock = document.querySelector(".left-dock");
      const toggleMenu = (open) => {
        const shouldOpen = open !== undefined ? open : !leftDock.classList.contains("mobile-open");
        leftDock.classList.toggle("mobile-open", shouldOpen);
        menuBackdrop.classList.toggle("open", shouldOpen);
        document.getElementById("m-btn-menu").classList.toggle("active", shouldOpen);
      };

      document.getElementById("m-btn-menu").addEventListener("click", () => toggleMenu());
      menuBackdrop.addEventListener("click", () => toggleMenu(false));

      // Close mobile menu on teleport button clicks
      document.querySelectorAll("[data-teleport]").forEach(btn => {
        btn.addEventListener("click", () => toggleMenu(false));
      });

      // --- VIRTUAL JOYSTICK TOUCH LISTENERS ---
      joystickZone.addEventListener("touchstart", (e) => {
        e.preventDefault();
        sound.init();
        const touch = e.changedTouches[0];
        touchJoystickId = touch.identifier;
        touchJoystickActive = true;

        const rect = joystickBase.getBoundingClientRect();
        joystickOriginX = rect.left + rect.width / 2;
        joystickOriginY = rect.top + rect.height / 2;
        handleJoystickMove(touch.clientX, touch.clientY);
      }, { passive: false });

      window.addEventListener("touchmove", (e) => {
        for (let i = 0; i < e.changedTouches.length; i++) {
          const t = e.changedTouches[i];
          if (touchJoystickActive && t.identifier === touchJoystickId) {
            handleJoystickMove(t.clientX, t.clientY);
          }
        }
      }, { passive: false });

      const endJoystick = (e) => {
        for (let i = 0; i < e.changedTouches.length; i++) {
          if (e.changedTouches[i].identifier === touchJoystickId) {
            touchJoystickActive = false;
            touchJoystickId = null;
            joystickVector.set(0, 0);
            joystickStick.style.transform = `translate(0px, 0px)`;
          }
        }
      };

      window.addEventListener("touchend", endJoystick);
      window.addEventListener("touchcancel", endJoystick);

      function handleJoystickMove(clientX, clientY) {
        const maxRadius = 40;
        let dx = clientX - joystickOriginX;
        let dy = clientY - joystickOriginY;
        const dist = Math.hypot(dx, dy);

        if (dist > maxRadius) {
          dx = (dx / dist) * maxRadius;
          dy = (dy / dist) * maxRadius;
        }

        joystickStick.style.transform = `translate(${dx}px, ${dy}px)`;
        // Normalize vector (-1 to 1)
        joystickVector.set(dx / maxRadius, -dy / maxRadius);
      }

      // --- TOUCH CAMERA LOOK (SWIPE RIGHT HALF OF SCREEN) ---
      renderer.domElement.addEventListener("touchstart", (e) => {
        sound.init();
        if (e.touches.length === 2) {
          // Pinch gesture start
          const dx = e.touches[0].clientX - e.touches[1].clientX;
          const dy = e.touches[0].clientY - e.touches[1].clientY;
          initialPinchDistance = Math.hypot(dx, dy);
          return;
        }

        for (let i = 0; i < e.changedTouches.length; i++) {
          const touch = e.changedTouches[i];
          // If touch is on right 65% of screen, use for camera look
          if (touch.clientX > window.innerWidth * 0.35 && !touchLookActive) {
            touchLookId = touch.identifier;
            touchLookActive = true;
            prevTouchLookX = touch.clientX;
            prevTouchLookY = touch.clientY;
          }
        }
      }, { passive: true });

      renderer.domElement.addEventListener("touchmove", (e) => {
        // Pinch-to-zoom
        if (e.touches.length === 2 && initialPinchDistance !== null) {
          const dx = e.touches[0].clientX - e.touches[1].clientX;
          const dy = e.touches[0].clientY - e.touches[1].clientY;
          const curDist = Math.hypot(dx, dy);
          const diff = (curDist - initialPinchDistance) * 0.01;
          camDistanceSetting = Math.max(1.8, Math.min(6.0, camDistanceSetting - diff));
          initialPinchDistance = curDist;
          return;
        }

        if (touchLookActive && isGameMode) {
          for (let i = 0; i < e.changedTouches.length; i++) {
            const touch = e.changedTouches[i];
            if (touch.identifier === touchLookId) {
              const dx = touch.clientX - prevTouchLookX;
              const dy = touch.clientY - prevTouchLookY;
              prevTouchLookX = touch.clientX;
              prevTouchLookY = touch.clientY;

              playerRotY -= dx * 0.007;
              cameraPitch = Math.max(-0.4, Math.min(0.75, cameraPitch + dy * 0.006));
            }
          }
        }
      }, { passive: true });

      const endTouchLook = (e) => {
        if (e.touches.length < 2) {
          initialPinchDistance = null;
        }
        for (let i = 0; i < e.changedTouches.length; i++) {
          if (e.changedTouches[i].identifier === touchLookId) {
            touchLookActive = false;
            touchLookId = null;
          }
        }
      };

      renderer.domElement.addEventListener("touchend", endTouchLook);
      renderer.domElement.addEventListener("touchcancel", endTouchLook);
    }

    function init() {
      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x080c16);
      scene.fog = new THREE.FogExp2(0x080c16, 0.005);

      camera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.1, 1000);

      renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.15;
      container.appendChild(renderer.domElement);

      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.08;
      controls.enabled = false;

      floor1Group = new THREE.Group();
      floor2Group = new THREE.Group();
      groundGroup = new THREE.Group();
      stairsMeshGroup = new THREE.Group();
      labelsGroup = new THREE.Group();

      scene.add(groundGroup);
      scene.add(floor1Group);
      scene.add(floor2Group);
      scene.add(stairsMeshGroup);
      scene.add(labelsGroup);

      // STACK FLOOR 2 DIRECTLY ON TOP OF FLOOR 1
      floor1Group.position.set(0, 0, 0);
      floor2Group.position.set(0, FLOOR_HEIGHT, 0);

      setupLighting();
      buildOutdoorGround();

      // Build Floor 1 and Floor 2 with complete, accurate walls
      buildHospitalFloor(1, floor1Group);
      buildHospitalFloor(2, floor2Group);

      // Dog-leg Stairs (correct enclosure, no blocking walls)
      buildDogLegStaircase();
      buildElevatorCabin();

      // Build Wall Labels and Signage (Color-coded)
      buildColoredWallLabels();

      // Playable Doctor Character
      createPlayerCharacter();

      setupEvents();
      setupUI();

      updateFloorVisibility();
      initDrawingSystem();
      initMobileControls();
      drawMinimap();
      animate();
    }

    // --- 6. LIGHTING (REALISTIC HOSPITAL ILLUMINATION) ---
    function setupLighting() {
      // Natural ambient / sky lighting
      const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e293b, 0.75);
      scene.add(hemiLight);

      // Sun directional light casting sharp soft shadows
      const dirLight = new THREE.DirectionalLight(0xfffaed, 0.95);
      dirLight.position.set(35, 55, -25);
      dirLight.castShadow = true;
      const isMobileDev = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent) || window.innerWidth <= 768;
      dirLight.shadow.mapSize.width = isMobileDev ? 1024 : 4096;
      dirLight.shadow.mapSize.height = isMobileDev ? 1024 : 4096;
      dirLight.shadow.camera.near = 5;
      dirLight.shadow.camera.far = 160;
      const d = 48;
      dirLight.shadow.camera.left = -d; dirLight.shadow.camera.right = d;
      dirLight.shadow.camera.top = d; dirLight.shadow.camera.bottom = -d;
      dirLight.shadow.bias = -0.0003;
      scene.add(dirLight);

      const ambient = new THREE.AmbientLight(0xffffff, 0.35);
      scene.add(ambient);

      // Recessed LED Corridor Troffer Lights
      [6, 12, 18, 24, 30, 36].forEach(lx => {
        // Floor 1 Lights
        addCeilingLight(floor1Group, lx, 2.75, 7.0);
        addCeilingLight(floor1Group, lx, 2.75, 18.0);
        // Floor 2 Lights
        addCeilingLight(floor2Group, lx, 2.75, 7.0);
        addCeilingLight(floor2Group, lx, 2.75, 18.0);
      });
    }

    function addCeilingLight(group, x, y, z) {
      // 3D LED Troffer Fixture (1.2m x 0.5m recessed panel)
      const fixture = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.04, 0.5), ceilingPanelMat);
      fixture.position.set(x, y, z);
      group.add(fixture);

      // Soft downward point light
      const p = new THREE.PointLight(0xf8fafc, 0.45, 9, 2);
      p.position.set(x, y - 0.15, z);
      group.add(p);
    }

    // --- 7. OUTDOOR ENVIRONMENT ---
    function buildOutdoorGround() {
      const groundGeo = new THREE.PlaneGeometry(180, 180);
      const groundMat = new THREE.MeshStandardMaterial({ color: 0x111622, roughness: 0.95 });
      const ground = new THREE.Mesh(groundGeo, groundMat);
      ground.rotation.x = -Math.PI / 2;
      ground.position.set(20, -0.05, 12.5);
      ground.receiveShadow = true;
      groundGroup.add(ground);

      const curbGeo = new THREE.BoxGeometry(48, 0.16, 36);
      const curbMat = new THREE.MeshStandardMaterial({ color: 0x1e2534, roughness: 0.8 });
      const curb = new THREE.Mesh(curbGeo, curbMat);
      curb.position.set(20, -0.02, 12.5);
      curb.receiveShadow = true;
      groundGroup.add(curb);

      // Asphalt ambulance driveway
      const driveMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 });
      const driveway = new THREE.Mesh(new THREE.BoxGeometry(10, 0.18, 12), driveMat);
      driveway.position.set(20, -0.01, -4);
      groundGroup.add(driveway);

      // Trees and landscaping
      const treeMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.8 });
      const trunkMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 });
      [[-4, -4], [-4, 8], [-4, 20], [44, -4], [44, 8], [44, 20], [10, -5], [30, -5]].forEach(([tx, tz]) => {
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 1.2), trunkMat);
        trunk.position.set(tx, 0.5, tz);
        trunk.castShadow = true;
        groundGroup.add(trunk);

        const foliage = new THREE.Mesh(new THREE.DodecahedronGeometry(0.85, 1), treeMat);
        foliage.position.set(tx, 1.6, tz);
        foliage.castShadow = true;
        groundGroup.add(foliage);
      });
    }

    // --- 8. FLOOR BUILDER WITH COMPLETE WALL ARCHITECTURE ---
    function buildHospitalFloor(floorNum, group) {
      const baseY = (floorNum - 1) * FLOOR_HEIGHT;
      const isF1 = floorNum === 1;

      // 1. Floor Slabs
      if (isF1) {
        // Floor 1 solid base slab
        const slab = new THREE.Mesh(
          new THREE.BoxGeometry(40, 0.25, 25),
          floorSlabMat
        );
        slab.position.set(20, 0.125, 12.5);
        slab.receiveShadow = true;
        group.add(slab);
      } else {
        // Floor 2 slab WITH STAIRCASE HOLE & ELEVATOR OPENING
        // Left slab section (X: 0 to 13.0, full depth)
        const sLeft = new THREE.Mesh(new THREE.BoxGeometry(13.0, 0.25, 25), floorSlabMat);
        sLeft.position.set(6.5, 0.125, 12.5);
        sLeft.receiveShadow = true;
        group.add(sLeft);

        // Central Lobby section between stairs and elevator (X: 17.5 to 22.0)
        const sLobby = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.25, 25), floorSlabMat);
        sLobby.position.set(19.75, 0.125, 12.5);
        sLobby.receiveShadow = true;
        group.add(sLobby);

        // Right Wing & Corridor slab (X: 25.5 to 40.0, full depth)
        const sRight = new THREE.Mesh(new THREE.BoxGeometry(14.5, 0.25, 25), floorSlabMat);
        sRight.position.set(32.75, 0.125, 12.5);
        sRight.receiveShadow = true;
        group.add(sRight);

        // North bridge over stairwell (X: 13.0 to 17.5, Z: 16.5 to 25.0)
        const sNorthStairs = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.25, 8.5), floorSlabMat);
        sNorthStairs.position.set(15.25, 0.125, 20.75);
        sNorthStairs.receiveShadow = true;
        group.add(sNorthStairs);

        // South bridge below stairwell (X: 13.0 to 17.5, Z: 0 to 8.0)
        const sSouthStairs = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.25, 8.0), floorSlabMat);
        sSouthStairs.position.set(15.25, 0.125, 4.0);
        sSouthStairs.receiveShadow = true;
        group.add(sSouthStairs);

        // North bridge over elevator (X: 22.0 to 25.5, Z: 15.5 to 25.0)
        const sNorthElev = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.25, 9.5), floorSlabMat);
        sNorthElev.position.set(23.75, 0.125, 20.25);
        sNorthElev.receiveShadow = true;
        group.add(sNorthElev);

        // South bridge below elevator (X: 22.0 to 25.5, Z: 0 to 9.5)
        const sSouthElev = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.25, 9.5), floorSlabMat);
        sSouthElev.position.set(23.75, 0.125, 4.75);
        sSouthElev.receiveShadow = true;
        group.add(sSouthElev);
      }

      // 2. Room Floor Accent Tiles & Furniture
      const rooms = ROOM_DATA.filter(r => r.floor === floorNum);
      rooms.forEach(room => {
        const tile = new THREE.Mesh(
          new THREE.BoxGeometry(room.w - 0.08, 0.04, room.d - 0.08),
          new THREE.MeshStandardMaterial({ color: room.color, roughness: 0.28, metalness: 0.06 })
        );
        tile.position.set(room.x + room.w / 2, 0.27, room.z + room.d / 2);
        tile.receiveShadow = true;
        tile.userData = { roomData: room };
        group.add(tile);
        roomMeshes.push(tile);

        addRoomProps(room, group);
      });

      // 3. BUILD ALL WALLS WITH INDIVIDUAL MATERIALS (FOR WALL OCCLUSION FADING)
      buildAllWalls(floorNum, group, baseY);

      // Entrance Canopy on Floor 1
      if (isF1) {
        const canopy = new THREE.Mesh(new THREE.BoxGeometry(7.2, 0.25, 3.2), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4 }));
        canopy.position.set(20, 2.7, -1.6);
        canopy.castShadow = true;
        group.add(canopy);
      }
    }

    function addWallSegment(x, z, w, d, group, baseY, isF1, isExt = false) {
      const h = WALL_HEIGHT;

      // Create an independent cloned material per wall segment so we can fade occluding walls individually!
      const wallColor = isExt ? 0xdde3ea : (isF1 ? 0xf8fafc : 0xf1f5f9);
      const wallMat = new THREE.MeshStandardMaterial({
        color: wallColor,
        roughness: 0.55,
        metalness: 0.04,
        bumpMap: wallStuccoTex,
        bumpScale: 0.02,
        transparent: false,
        opacity: 1.0,
        depthWrite: true
      });

      const wallMesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat);
      wallMesh.position.set(x + w / 2, 0.25 + h / 2, z + d / 2);
      wallMesh.castShadow = true;
      wallMesh.receiveShadow = true;
      wallMesh.userData = {
        isWall: true,
        floor: isF1 ? 1 : 2,
        baseOpacity: 1.0,
        currentOpacity: 1.0
      };
      group.add(wallMesh);
      allWallMeshes.push(wallMesh);

      // Baseboard kickplate (14cm architectural trim)
      const baseboardMesh = new THREE.Mesh(new THREE.BoxGeometry(w + 0.02, 0.14, d + 0.02), baseboardMat);
      baseboardMesh.position.set(x + w / 2, 0.25 + 0.07, z + d / 2);
      group.add(baseboardMesh);

      // Corridor Wall Bumper Crash Rail (Hospital protective rail at 0.88m height)
      if (!isExt) {
        const bumperMesh = new THREE.Mesh(new THREE.BoxGeometry(w + 0.04, 0.12, d + 0.04), bumperRailMat);
        bumperMesh.position.set(x + w / 2, 0.25 + 0.88, z + d / 2);
        group.add(bumperMesh);
      }

      // Register collision box for character movement
      wallColliders.push({
        minX: x - 0.12,
        maxX: x + w + 0.12,
        minZ: z - 0.12,
        maxZ: z + d + 0.12,
        minY: baseY,
        maxY: baseY + h
      });
    }

    function addDoorHeader(x, z, w, d, group, baseY, isF1) {
      const h = WALL_HEIGHT - 2.1; // 0.7m header spanning above doorway (from Y = 2.1m to 2.8m)
      const wallColor = isF1 ? 0xf8fafc : 0xf1f5f9;
      const wallMat = new THREE.MeshStandardMaterial({
        color: wallColor,
        roughness: 0.55,
        metalness: 0.04,
        bumpMap: wallStuccoTex,
        bumpScale: 0.02,
        transparent: false,
        opacity: 1.0,
        depthWrite: true
      });
      const headerMesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat);
      headerMesh.position.set(x + w / 2, baseY + 2.1 + h / 2, z + d / 2);
      headerMesh.castShadow = true;
      headerMesh.receiveShadow = true;
      headerMesh.userData = { isWall: true, floor: isF1 ? 1 : 2, baseOpacity: 1.0, currentOpacity: 1.0 };
      group.add(headerMesh);
      allWallMeshes.push(headerMesh);
      // NOTE: No entry in wallColliders below 2.1m so player walks through freely!
    }


    function buildAllWalls(floorNum, group, baseY) {
      const isF1 = floorNum === 1;
      const wt = 0.22;

      // 1. EXTERIOR BOUNDARY WALLS
      if (isF1) {
        addWallSegment(0, 0, 18, wt, group, baseY, isF1, true);
        addWallSegment(22, 0, 18, wt, group, baseY, isF1, true); // Main entrance gap 18 to 22
        addDoorHeader(18, 0, 4.0, wt, group, baseY, isF1); // Canopy header above entrance
      } else {
        addWallSegment(0, 0, 40, wt, group, baseY, isF1, true);
      }
      addWallSegment(0, 25 - wt, 40, wt, group, baseY, isF1, true);
      addWallSegment(0, 0, wt, 25, group, baseY, isF1, true);
      addWallSegment(40 - wt, 0, wt, 25, group, baseY, isF1, true);

      // 2. SOUTH ROW WALLS (Z = 6.0) WITH GENEROUS ARCHITECTURAL DOORWAYS
      if (isF1) {
        addWallSegment(0, 6 - wt, 4.4, wt, group, baseY, isF1);
        addDoorHeader(4.4, 6 - wt, 1.6, wt, group, baseY, isF1); // Door 112 Restroom
        addWallSegment(6.0, 6 - wt, 5.2, wt, group, baseY, isF1);
        addDoorHeader(11.2, 6 - wt, 2.3, wt, group, baseY, isF1); // Door 113 Cafeteria
        addWallSegment(13.5, 6 - wt, 3.5, wt, group, baseY, isF1);
        addDoorHeader(17.0, 6 - wt, 2.5, wt, group, baseY, isF1); // Door 114 Waiting Area
        addWallSegment(19.5, 6 - wt, 3.2, wt, group, baseY, isF1);
        addDoorHeader(22.7, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 115 Info Desk
        addWallSegment(24.5, 6 - wt, 4.2, wt, group, baseY, isF1);
        addDoorHeader(28.7, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 116 Administration
        addWallSegment(30.5, 6 - wt, 9.5, wt, group, baseY, isF1);

        // South room internal dividers
        addWallSegment(7, 0, wt, 6, group, baseY, isF1);
        addWallSegment(17, 0, wt, 6, group, baseY, isF1);
        addWallSegment(23, 0, wt, 6, group, baseY, isF1);
        addWallSegment(29, 0, wt, 6, group, baseY, isF1);
      } else {
        addWallSegment(0, 6 - wt, 5.2, wt, group, baseY, isF1);
        addDoorHeader(5.2, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 212 Conference
        addWallSegment(7.0, 6 - wt, 4.2, wt, group, baseY, isF1);
        addDoorHeader(11.2, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 213 Training
        addWallSegment(13.0, 6 - wt, 4.2, wt, group, baseY, isF1);
        addDoorHeader(17.2, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 214 Pantry
        addWallSegment(19.0, 6 - wt, 4.2, wt, group, baseY, isF1);
        addDoorHeader(23.2, 6 - wt, 1.8, wt, group, baseY, isF1); // Door 215 Restroom
        addWallSegment(25.0, 6 - wt, 5.8, wt, group, baseY, isF1);
        addDoorHeader(30.8, 6 - wt, 1.7, wt, group, baseY, isF1); // Door 216 Staff Lounge
        addWallSegment(32.5, 6 - wt, 7.5, wt, group, baseY, isF1);

        addWallSegment(9, 0, wt, 6, group, baseY, isF1);
        addWallSegment(16, 0, wt, 6, group, baseY, isF1);
        addWallSegment(22, 0, wt, 6, group, baseY, isF1);
        addWallSegment(28, 0, wt, 6, group, baseY, isF1);
      }

      // 3. NORTH ROW WALLS (Z = 19.0) WITH GENEROUS ARCHITECTURAL DOORWAYS
      if (isF1) {
        addWallSegment(0, 19, 5.0, wt, group, baseY, isF1);
        addDoorHeader(5.0, 19, 2.0, wt, group, baseY, isF1); // Door 101 Emergency
        addWallSegment(7.0, 19, 1.4, wt, group, baseY, isF1);
        addDoorHeader(8.4, 19, 1.8, wt, group, baseY, isF1); // Door 102 Reception
        addWallSegment(10.2, 19, 4.1, wt, group, baseY, isF1);
        addDoorHeader(14.3, 19, 1.9, wt, group, baseY, isF1); // Door 103 OPD
        addWallSegment(16.2, 19, 3.8, wt, group, baseY, isF1);
        addDoorHeader(20.0, 19, 1.8, wt, group, baseY, isF1); // Door 104 Pharmacy
        addWallSegment(21.8, 19, 3.2, wt, group, baseY, isF1);
        addDoorHeader(25.0, 19, 1.8, wt, group, baseY, isF1); // Door 105 Lab
        addWallSegment(26.8, 19, 3.5, wt, group, baseY, isF1);
        addDoorHeader(30.3, 19, 1.9, wt, group, baseY, isF1); // Door 106 Radiology
        addWallSegment(32.2, 19, 3.6, wt, group, baseY, isF1);
        addDoorHeader(35.8, 19, 2.0, wt, group, baseY, isF1); // Door 107 Ultrasound
        addWallSegment(37.8, 19, 2.2, wt, group, baseY, isF1);

        addWallSegment(7, 19, wt, 6, group, baseY, isF1);
        addWallSegment(13, 19, wt, 6, group, baseY, isF1);
        addWallSegment(19, 19, wt, 6, group, baseY, isF1);
        addWallSegment(24, 19, wt, 6, group, baseY, isF1);
        addWallSegment(29, 19, wt, 6, group, baseY, isF1);
        addWallSegment(34.5, 19, wt, 6, group, baseY, isF1);
      } else {
        addWallSegment(0, 19, 5.0, wt, group, baseY, isF1);
        addDoorHeader(5.0, 19, 2.0, wt, group, baseY, isF1); // Door 201 ICU
        addWallSegment(7.0, 19, 1.2, wt, group, baseY, isF1);
        addDoorHeader(8.2, 19, 1.8, wt, group, baseY, isF1); // Door 202 ICU Support
        addWallSegment(10.0, 19, 3.8, wt, group, baseY, isF1);
        addDoorHeader(13.8, 19, 2.0, wt, group, baseY, isF1); // Door 203 OT 1
        addWallSegment(15.8, 19, 4.8, wt, group, baseY, isF1);
        addDoorHeader(20.6, 19, 2.2, wt, group, baseY, isF1); // Door 204 OT 2
        addWallSegment(22.8, 19, 4.4, wt, group, baseY, isF1);
        addDoorHeader(27.2, 19, 2.0, wt, group, baseY, isF1); // Door 205 Sterilization
        addWallSegment(29.2, 19, 4.8, wt, group, baseY, isF1);
        addDoorHeader(34.0, 19, 2.0, wt, group, baseY, isF1); // Door 206 Maternity
        addWallSegment(36.0, 19, 4.0, wt, group, baseY, isF1);

        addWallSegment(7, 19, wt, 6, group, baseY, isF1);
        addWallSegment(12, 19, wt, 6, group, baseY, isF1);
        addWallSegment(19, 19, wt, 6, group, baseY, isF1);
        addWallSegment(26, 19, wt, 6, group, baseY, isF1);
        addWallSegment(32, 19, wt, 6, group, baseY, isF1);
      }

      // 4. CENTRAL LEFT WING (CARDIOLOGY 108 & GENERAL WARD 109)
      // North Wall along Z = 17 - wt, South Wall along Z = 8
      addWallSegment(0, 17 - wt, 11, wt, group, baseY, isF1);
      addWallSegment(0, 8, 11, wt, group, baseY, isF1);

      // East Wall along X = 11 with doors and door headers facing the corridor
      if (isF1) {
        addWallSegment(11, 8.0, wt, 1.2, group, baseY, isF1);
        addDoorHeader(11, 9.2, wt, 1.8, group, baseY, isF1); // DOOR 109 General Ward (Z: 9.2-11.0)
        addWallSegment(11, 11.0, wt, 2.6, group, baseY, isF1);
        addDoorHeader(11, 13.6, wt, 1.8, group, baseY, isF1); // DOOR 108 Cardiology (Z: 13.6-15.4)
        addWallSegment(11, 15.4, wt, 1.6, group, baseY, isF1);
        addWallSegment(0, 12.5, 11, wt, group, baseY, isF1); // Horizontal divider between 108 & 109
      } else {
        // Floor 2 Doctors' Offices 207, 208, 209
        addWallSegment(11, 8.0, wt, 1.0, group, baseY, isF1);
        addDoorHeader(11, 9.0, wt, 1.6, group, baseY, isF1); // DOOR 209 (Z: 9.0-10.6)
        addWallSegment(11, 10.6, wt, 1.4, group, baseY, isF1);
        addDoorHeader(11, 12.0, wt, 1.6, group, baseY, isF1); // DOOR 208 (Z: 12.0-13.6)
        addWallSegment(11, 13.6, wt, 1.4, group, baseY, isF1);
        addDoorHeader(11, 15.0, wt, 1.6, group, baseY, isF1); // DOOR 207 (Z: 15.0-16.6)
        addWallSegment(11, 16.6, wt, 0.4, group, baseY, isF1);
        addWallSegment(0, 11.0, 11, wt, group, baseY, isF1); // Dividers
        addWallSegment(0, 14.0, 11, wt, group, baseY, isF1);
      }

      // 5. CENTRAL RIGHT WING (ISOLATION ROOM 111 & GENERAL WARD 110)
      // North Wall along Z = 17 - wt, South Wall along Z = 8
      addWallSegment(29, 17 - wt, 11, wt, group, baseY, isF1);
      addWallSegment(29, 8, 11, wt, group, baseY, isF1);

      // West Wall along X = 29 - wt with doors and door headers facing the hallway
      if (isF1) {
        addWallSegment(29 - wt, 8.0, wt, 1.2, group, baseY, isF1);
        addDoorHeader(29 - wt, 9.2, wt, 1.8, group, baseY, isF1); // CLEAR DOORWAY 111 Isolation Room (Z: 9.2-11.0)
        addWallSegment(29 - wt, 11.0, wt, 2.6, group, baseY, isF1);
        addDoorHeader(29 - wt, 13.6, wt, 1.8, group, baseY, isF1); // CLEAR DOORWAY 110 General Ward (Z: 13.6-15.4)
        addWallSegment(29 - wt, 15.4, wt, 1.6, group, baseY, isF1);
        addWallSegment(29, 12.5, 11, wt, group, baseY, isF1); // Horizontal divider between 110 & 111
      } else {
        // Floor 2 Pediatrics Wards 210 & 211
        addWallSegment(29 - wt, 8.0, wt, 1.2, group, baseY, isF1);
        addDoorHeader(29 - wt, 9.2, wt, 1.8, group, baseY, isF1); // DOORWAY 211 Pediatrics
        addWallSegment(29 - wt, 11.0, wt, 2.6, group, baseY, isF1);
        addDoorHeader(29 - wt, 13.6, wt, 1.8, group, baseY, isF1); // DOORWAY 210 Pediatrics
        addWallSegment(29 - wt, 15.4, wt, 1.6, group, baseY, isF1);
        addWallSegment(29, 12.5, 11, wt, group, baseY, isF1); // Divider
      }

      // 6. STAIRCASE ENCLOSURE WALLS (U-SHAPE, SOUTH OPEN)
      addWallSegment(13, 8, wt, 8.5, group, baseY, isF1); // West wall
      addWallSegment(13, 16.5 - wt, 4.5, wt, group, baseY, isF1); // North wall
      addWallSegment(17.5 - wt, 8, wt, 8.5, group, baseY, isF1); // East wall

      // 7. LOBBY SOUTH WALL (ALONG Z = 8.0)
      addWallSegment(17.5, 8, 3.0, wt, group, baseY, isF1);
      // (Wide opening at X: 20.5 to 22.0 for Lobby Entrance)

      // 8. ELEVATOR SHAFT ENCLOSURE WALLS (STANDALONE TOWER AT X: 22.0 to 25.5, Z: 9.5 to 15.5)
      // Completely leaves X: 25.5 to 29.0 open as a wide 3.5m corridor leading to Isolation Room & General Ward!
      addWallSegment(22.0, 9.5, wt, 6.0, group, baseY, isF1); // West wall of elevator
      addWallSegment(22.0, 15.5 - wt, 3.5, wt, group, baseY, isF1); // North wall of elevator
      addWallSegment(25.5 - wt, 9.5, wt, 6.0, group, baseY, isF1); // East wall of elevator (DOES NOT TOUCH X = 29!)
      // South elevator entrance doorway
      addWallSegment(22.0, 9.5, 0.7, wt, group, baseY, isF1);
      addDoorHeader(22.7, 9.5, 2.1, wt, group, baseY, isF1); // 2.1m wide elevator door opening
      addWallSegment(24.8, 9.5, 0.7, wt, group, baseY, isF1);
    }

    // --- 9. DOG-LEG STAIRCASE ---
    function buildDogLegStaircase() {
      const stepMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.4, roughness: 0.35 });
      const landingMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.3, roughness: 0.45 });
      const railMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.85, roughness: 0.2 });

      // Flight 1: Left flight goes UP from South (Z = 8.2) to North (Z = 14.5)
      const numStepsFlight = 10;
      const stepDepth = (14.5 - 8.2) / numStepsFlight;
      const stepHeight = (FLOOR_HEIGHT / 2) / numStepsFlight;

      for (let i = 0; i < numStepsFlight; i++) {
        const step = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.16, stepDepth), stepMat);
        step.position.set(14.1, 0.08 + i * stepHeight, 8.2 + i * stepDepth + stepDepth / 2);
        step.castShadow = true;
        step.receiveShadow = true;
        stairsMeshGroup.add(step);
      }

      // Half-Landing at North (Z = 14.5 to 16.3, X = 13.1 to 17.3, Y = 1.8m)
      const landing = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.18, 1.8), landingMat);
      landing.position.set(15.2, FLOOR_HEIGHT / 2, 15.4);
      landing.castShadow = true;
      landing.receiveShadow = true;
      stairsMeshGroup.add(landing);

      // Flight 2: Right flight goes UP from North (Z = 14.5) to South (Z = 8.2)
      for (let i = 0; i < numStepsFlight; i++) {
        const step = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.16, stepDepth), stepMat);
        step.position.set(16.3, FLOOR_HEIGHT / 2 + 0.08 + i * stepHeight, 14.5 - i * stepDepth - stepDepth / 2);
        step.castShadow = true;
        step.receiveShadow = true;
        stairsMeshGroup.add(step);
      }

      // Central Divider Railing
      const centerRail = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.0, 6.4), railMat);
      centerRail.position.set(15.2, FLOOR_HEIGHT / 2 + 0.4, 11.4);
      stairsMeshGroup.add(centerRail);
    }

    // --- 10. ELEVATOR CABIN ---
    function buildElevatorCabin() {
      elevatorCabin = new THREE.Group();
      const floor = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.15, 4.4), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.3 }));
      floor.position.y = 0.1;
      elevatorCabin.add(floor);

      const glassWallBack = new THREE.Mesh(new THREE.BoxGeometry(2.6, 2.6, 0.08), glassMat);
      glassWallBack.position.set(0, 1.4, 2.15);
      const glassWallSide1 = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.6, 4.4), glassMat);
      glassWallSide1.position.set(1.25, 1.4, 0);
      const glassWallSide2 = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.6, 4.4), glassMat);
      glassWallSide2.position.set(-1.25, 1.4, 0);
      elevatorCabin.add(glassWallBack, glassWallSide1, glassWallSide2);

      const elevCeil = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.1, 4.4), new THREE.MeshStandardMaterial({ color: 0x334155 }));
      elevCeil.position.y = 2.75;
      elevatorCabin.add(elevCeil);

      const elevLight = new THREE.PointLight(0xa5f3fc, 0.85, 6);
      elevLight.position.set(0, 2.5, 0);
      elevatorCabin.add(elevLight);

      elevatorCabin.position.set(23.75, 0, 12.5);
      scene.add(elevatorCabin);
    }

    // --- 11. COLOR-CODED WALL LABELS & SIGNAGE ---
    function createRoomSignTexture(room) {
      const canvas = document.createElement("canvas");
      canvas.width = 512;
      canvas.height = 256;
      const ctx = canvas.getContext("2d");

      const catInfo = CAT_COLORS[room.cat] || { css: "#0284c7", border: "#0369a1" };

      // Background rounded card
      ctx.fillStyle = "rgba(15, 23, 42, 0.94)";
      ctx.beginPath();
      ctx.roundRect(10, 10, 492, 236, 24);
      ctx.fill();

      // Glowing colored border
      ctx.lineWidth = 10;
      ctx.strokeStyle = catInfo.css;
      ctx.stroke();

      // Top colored banner pill for Room ID
      ctx.fillStyle = catInfo.css;
      ctx.beginPath();
      ctx.roundRect(30, 30, 150, 60, 14);
      ctx.fill();

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 36px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(room.id, 105, 60);

      // Category Pill Tag
      ctx.fillStyle = "rgba(255, 255, 255, 0.12)";
      ctx.beginPath();
      ctx.roundRect(200, 34, 270, 52, 12);
      ctx.fill();

      ctx.fillStyle = "#38bdf8";
      ctx.font = "bold 22px 'Inter', sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(room.cat.toUpperCase(), 220, 60);

      // Room Name (Large crisp white title)
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 38px 'Inter', sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(room.name, 34, 145);

      // Subtitle information (beds / equipment)
      ctx.fillStyle = "#94a3b8";
      ctx.font = "24px 'Inter', sans-serif";
      ctx.fillText(room.beds || "Active Care Suite", 34, 195);

      const tex = new THREE.CanvasTexture(canvas);
      tex.needsUpdate = true;
      return tex;
    }

    function buildColoredWallLabels() {
      // Clear previous labels if any
      while (labelsGroup.children.length > 0) {
        labelsGroup.remove(labelsGroup.children[0]);
      }

      ROOM_DATA.forEach(room => {
        // Skip corridor/stair/elevator utility markers from cluttering
        if (room.id.includes("Lobby") || room.id.includes("Stairs") || room.id.includes("Elevator")) return;

        const baseY = (room.floor - 1) * FLOOR_HEIGHT;
        const cx = room.x + room.w / 2;
        const cz = room.z + room.d / 2;
        const signTex = createRoomSignTexture(room);

        // 1. Floating 3D Billboard Label above room center
        const spriteMat = new THREE.SpriteMaterial({
          map: signTex,
          transparent: true,
          opacity: 0.95,
          depthTest: false
        });
        const sprite = new THREE.Sprite(spriteMat);
        sprite.position.set(cx, baseY + 2.5, cz);
        sprite.scale.set(2.4, 1.2, 1);
        sprite.userData = { room: room, isLabel: true };
        labelsGroup.add(sprite);

        // 2. Wall-mounted Door Plaque (Acrylic sign plate)
        // Positioned along the room entrance wall
        const plaqueGeo = new THREE.BoxGeometry(1.4, 0.7, 0.04);
        const plaqueMat = new THREE.MeshStandardMaterial({
          map: signTex,
          roughness: 0.2,
          metalness: 0.1
        });
        const plaque = new THREE.Mesh(plaqueGeo, plaqueMat);

        // Calculate precise plaque placement directly mounted above each room entrance door
        let px = cx;
        let pz = cz;
        let rotY = 0;

        if (room.z <= 6) {
          // South row rooms: door faces north into south corridor
          pz = 6.08;
          rotY = 0;
          if (room.id === "112") px = 5.2;
          else if (room.id === "113") px = 12.3;
          else if (room.id === "114") px = 18.2;
          else if (room.id === "115") px = 23.6;
          else if (room.id === "116") px = 29.6;
          else if (room.id === "212") px = 6.1;
          else if (room.id === "213") px = 12.1;
          else if (room.id === "214") px = 18.1;
          else if (room.id === "215") px = 24.1;
          else if (room.id === "216") px = 31.6;
        } else if (room.z >= 19) {
          // North row rooms: door faces south into north corridor
          pz = 18.92;
          rotY = Math.PI;
          if (room.id === "101") px = 6.0;
          else if (room.id === "102") px = 9.3;
          else if (room.id === "103") px = 15.2;
          else if (room.id === "104") px = 20.9;
          else if (room.id === "105") px = 25.9;
          else if (room.id === "106") px = 31.2;
          else if (room.id === "107") px = 36.8;
          else if (room.id === "201") px = 6.0;
          else if (room.id === "202") px = 9.1;
          else if (room.id === "203") px = 14.8;
          else if (room.id === "204") px = 21.7;
          else if (room.id === "205") px = 28.2;
          else if (room.id === "206") px = 35.0;
        } else if (room.x <= 11) {
          // Left wing rooms: door is on the East wall (X = 11.08), facing East into the corridor
          px = 11.08;
          rotY = Math.PI / 2;
          if (room.id === "109") pz = 10.1;
          else if (room.id === "108") pz = 14.5;
          else if (room.id === "209") pz = 9.8;
          else if (room.id === "208") pz = 12.8;
          else if (room.id === "207") pz = 15.8;
        } else {
          // Right wing rooms (Isolation Room 111 & General Ward 110): door is on the West wall (X = 28.92), facing West into the corridor
          px = 28.92;
          rotY = -Math.PI / 2;
          if (room.id === "111") pz = 10.1;
          else if (room.id === "110") pz = 14.5;
          else if (room.id === "211") pz = 10.1;
          else if (room.id === "210") pz = 14.5;
        }

        plaque.position.set(px, baseY + 2.35, pz);
        plaque.rotation.y = rotY;
        labelsGroup.add(plaque);
      });
    }

    // --- 12. HIGH-FIDELITY ROOM PROPS & MEDICAL EQUIPMENT ---
    const bedMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.28 });
    const blueMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.35 });
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x9a3412, roughness: 0.45 });
    const darkMetalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3 });
    const monitorScreenMat = new THREE.MeshStandardMaterial({
      color: 0x052e16,
      emissive: 0x10b981,
      emissiveIntensity: 0.8,
      roughness: 0.2
    });

    function addRoomProps(room, group) {
      const cx = room.x + room.w / 2;
      const cz = room.z + room.d / 2;

      if (room.id === "101" || room.id === "201") {
        // High-acuity trauma / ICU beds with vitals monitors and IV poles
        addDetailedHospitalBed(cx - 1.6, cz, group);
        addDetailedHospitalBed(cx + 1.6, cz, group);
        addVitalsMonitor(cx - 1.6, cz - 1.1, group);
        addVitalsMonitor(cx + 1.6, cz - 1.1, group);
        addIVDripStand(cx - 0.7, cz - 0.5, group);
        addIVDripStand(cx + 2.5, cz - 0.5, group);
      } else if (room.id === "109" || room.id === "110" || room.id === "206" || room.id === "210" || room.id === "211") {
        // Multi-bed ward
        addDetailedHospitalBed(cx - 2.4, cz, group);
        addDetailedHospitalBed(cx + 2.4, cz, group);
        addIVDripStand(cx - 1.6, cz, group);
        addIVDripStand(cx + 1.6, cz, group);
      } else if (room.id === "203" || room.id === "204") {
        // Surgical Suites (Operating Theatres)
        // Hydraulic operating table
        const opTable = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.8, 2.2), new THREE.MeshStandardMaterial({ color: 0x0d9488, roughness: 0.3, metalness: 0.4 }));
        opTable.position.set(cx, 0.5, cz);
        opTable.castShadow = true;
        group.add(opTable);

        // Dual articulated surgical scialytic lamps overhead
        const dome1 = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 0.15, 24), stainlessMat);
        dome1.position.set(cx - 0.6, 2.3, cz);
        group.add(dome1);
        const domeLight1 = new THREE.PointLight(0xa5f3fc, 0.9, 5);
        domeLight1.position.set(cx - 0.6, 2.15, cz);
        group.add(domeLight1);

        const dome2 = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 0.15, 24), stainlessMat);
        dome2.position.set(cx + 0.6, 2.3, cz);
        group.add(dome2);
        const domeLight2 = new THREE.PointLight(0xa5f3fc, 0.9, 5);
        domeLight2.position.set(cx + 0.6, 2.15, cz);
        group.add(domeLight2);

        // Anesthesia workstation
        const cart = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.3, 0.8), darkMetalMat);
        cart.position.set(cx - 1.8, 0.75, cz);
        group.add(cart);
      } else if (room.id === "106") {
        // CT / Radiology ring gantry
        const ctRing = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.38, 16, 32), bedMat);
        ctRing.position.set(cx, 1.4, cz);
        ctRing.rotation.y = Math.PI / 2;
        ctRing.castShadow = true;
        group.add(ctRing);

        // Motorized sliding patient couch
        const couch = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.65, 2.4), darkMetalMat);
        couch.position.set(cx, 0.4, cz - 0.4);
        group.add(couch);
      } else if (room.id === "113") {
        // Cafeteria dining tables
        [-2.5, 0, 2.5].forEach(ox => {
          const table = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 0.75, 16), woodMat);
          table.position.set(cx + ox, 0.45, cz);
          table.castShadow = true;
          group.add(table);
        });
      } else if (room.id === "212") {
        // Boardroom conference table
        const confTable = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.78, 1.8), woodMat);
        confTable.position.set(cx, 0.48, cz);
        confTable.castShadow = true;
        group.add(confTable);
      } else if (room.id === "102" || room.id === "115") {
        // Reception & Info service counters
        const counter = new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.0, 0.8), woodMat);
        counter.position.set(cx, 0.6, cz);
        counter.castShadow = true;
        group.add(counter);
      } else if (room.id === "108" || room.id === "207" || room.id === "208" || room.id === "209") {
        // Doctor consultation desks
        const desk = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.75, 0.9), woodMat);
        desk.position.set(cx - 1.2, 0.48, cz);
        group.add(desk);

        const examTable = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.65, 1.9), blueMat);
        examTable.position.set(cx + 1.8, 0.42, cz);
        group.add(examTable);
      }
    }

    function addDetailedHospitalBed(x, z, group) {
      // Bed base frame
      const frame = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.35, 2.2), darkMetalMat);
      frame.position.set(x, 0.28, z);
      frame.castShadow = true;
      group.add(frame);

      // Mattress
      const mattress = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.22, 2.05), bedMat);
      mattress.position.set(x, 0.52, z);
      mattress.castShadow = true;
      group.add(mattress);

      // Ergonomic clinical pillow
      const pillow = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.12, 0.45), blueMat);
      pillow.position.set(x, 0.67, z + 0.7);
      group.add(pillow);

      // Chrome safety side-rails
      const railL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.28, 1.4), stainlessMat);
      railL.position.set(x - 0.54, 0.65, z);
      const railR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.28, 1.4), stainlessMat);
      railR.position.set(x + 0.54, 0.65, z);
      group.add(railL, railR);
    }

    function addVitalsMonitor(x, z, group) {
      const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.4), stainlessMat);
      stand.position.set(x, 0.8, z);
      group.add(stand);

      const monitor = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.32, 0.12), darkMetalMat);
      monitor.position.set(x, 1.5, z);
      group.add(monitor);

      const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.36, 0.26), monitorScreenMat);
      screen.position.set(x, 1.5, z + 0.07);
      group.add(screen);
    }

    function addIVDripStand(x, z, group) {
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 1.8), stainlessMat);
      pole.position.set(x, 0.9, z);
      group.add(pole);

      // Saline fluid infusion bag
      const bag = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.25, 0.08), glassMat);
      bag.position.set(x, 1.7, z);
      group.add(bag);
    }

    // --- 13. PLAYABLE DOCTOR CHARACTER ---
    let playerLegL, playerLegR, playerArmL, playerArmR, playerBody;
    function createPlayerCharacter() {
      player = new THREE.Group();

      const coatMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.45 });
      const scrubsMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.55 });
      const skinMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.5 });
      const hairMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 });

      playerBody = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.65, 0.28), coatMat);
      playerBody.position.y = 0.95;
      playerBody.castShadow = true;
      player.add(playerBody);

      const steth = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.025, 8, 16), new THREE.MeshStandardMaterial({ color: 0x334155 }));
      steth.rotation.x = Math.PI / 2;
      steth.position.set(0, 1.25, 0.05);
      player.add(steth);

      const badge = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.12, 0.02), blueMat);
      badge.position.set(0.12, 1.1, 0.15);
      player.add(badge);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.28, 0.28), skinMat);
      head.position.y = 1.45;
      head.castShadow = true;
      player.add(head);

      const hair = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 0.3), hairMat);
      hair.position.y = 1.6;
      player.add(hair);

      const legGeo = new THREE.BoxGeometry(0.18, 0.65, 0.18);
      playerLegL = new THREE.Mesh(legGeo, scrubsMat);
      playerLegL.position.set(-0.13, 0.35, 0);
      playerLegL.castShadow = true;
      player.add(playerLegL);

      playerLegR = new THREE.Mesh(legGeo, scrubsMat);
      playerLegR.position.set(0.13, 0.35, 0);
      playerLegR.castShadow = true;
      player.add(playerLegR);

      const armGeo = new THREE.BoxGeometry(0.12, 0.55, 0.12);
      playerArmL = new THREE.Mesh(armGeo, coatMat);
      playerArmL.position.set(-0.32, 0.9, 0);
      playerArmL.castShadow = true;
      player.add(playerArmL);

      playerArmR = new THREE.Mesh(armGeo, coatMat);
      playerArmR.position.set(0.32, 0.9, 0);
      playerArmR.castShadow = true;
      player.add(playerArmR);

      player.position.copy(playerPos);
      player.rotation.y = playerRotY;
      scene.add(player);
    }

    // --- 14. SMOOTH MOVEMENT & CONGESTION PREVENTION ---
    let walkCycle = 0;
    let stepSoundTimer = 0;

    function updatePlayerMovement(delta) {
      if (!isGameMode) return;

      const moveSpeed = keys.shift ? 7.2 : 4.0;
      const moveVec = new THREE.Vector3();

      if (keys.w) moveVec.z += 1;
      if (keys.s) moveVec.z -= 1;
      if (keys.a) moveVec.x += 1;
      if (keys.d) moveVec.x -= 1;

      // Integrate Virtual Touch Joystick for mobile
      if (touchJoystickActive && joystickVector.lengthSq() > 0.01) {
        moveVec.z += joystickVector.y; // forward / backward
        moveVec.x -= joystickVector.x; // left / right strafe
      }

      const isMoving = moveVec.lengthSq() > 0.001;
      if (isMoving) {
        moveVec.normalize();
        const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotY);
        const right = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), playerRotY);

        const deltaMove = new THREE.Vector3()
          .addScaledVector(forward, moveVec.z * moveSpeed * delta)
          .addScaledVector(right, moveVec.x * moveSpeed * delta);

        const nextX = playerPos.x + deltaMove.x;
        const nextZ = playerPos.z + deltaMove.z;

        // Smooth sliding collision detection: test X and Z separately
        if (!checkWallCollision(nextX, playerPos.z, playerPos.y)) {
          playerPos.x = nextX;
        }
        if (!checkWallCollision(playerPos.x, nextZ, playerPos.y)) {
          playerPos.z = nextZ;
        }

        walkCycle += delta * (keys.shift ? 16 : 10);
        playerLegL.rotation.x = Math.sin(walkCycle) * 0.6;
        playerLegR.rotation.x = -Math.sin(walkCycle) * 0.6;
        playerArmL.rotation.x = -Math.sin(walkCycle) * 0.5;
        playerArmR.rotation.x = Math.sin(walkCycle) * 0.5;
        playerBody.position.y = 0.95 + Math.abs(Math.sin(walkCycle)) * 0.04;

        stepSoundTimer += delta;
        if (stepSoundTimer > (keys.shift ? 0.22 : 0.35)) {
          sound.playFootstep();
          stepSoundTimer = 0;
        }
      } else {
        playerLegL.rotation.x = 0;
        playerLegR.rotation.x = 0;
        playerArmL.rotation.x = 0;
        playerArmR.rotation.x = 0;
        playerBody.position.y = 0.95;
      }

      checkDogLegStairClimbing();
      checkElevatorProximity();

      player.position.copy(playerPos);
      player.rotation.y = playerRotY;

      updateCurrentRoomLocation();
      updateCamera(delta);
    }

    // SLIM COLLISION CAPSULE (0.20m radius) PREVENTS GETTING STUCK IN CONGESTED AREAS
    function checkWallCollision(px, pz, py) {
      const radius = 0.20;
      for (let i = 0; i < wallColliders.length; i++) {
        const c = wallColliders[i];
        if (py + 0.5 >= c.minY && py <= c.maxY) {
          if (px + radius > c.minX && px - radius < c.maxX &&
              pz + radius > c.minZ && pz - radius < c.maxZ) {
            return true;
          }
        }
      }
      return false;
    }

    function checkDogLegStairClimbing() {
      // Stairwell area: X = 13.0 to 17.5, Z = 8.0 to 16.5
      if (playerPos.x >= 13.1 && playerPos.x <= 17.4 && playerPos.z >= 8.0 && playerPos.z <= 16.5) {
        if (playerPos.x < 15.2) {
          // Left flight: walking North climbs from Y = 0 to 1.8m
          const t = Math.max(0, Math.min(1, (playerPos.z - 8.2) / (14.5 - 8.2)));
          playerPos.y = t * (FLOOR_HEIGHT / 2);
        } else {
          // Right flight: walking South climbs from Y = 1.8m to 3.6m (Floor 2)
          const t = Math.max(0, Math.min(1, (14.5 - playerPos.z) / (14.5 - 8.2)));
          playerPos.y = (FLOOR_HEIGHT / 2) + t * (FLOOR_HEIGHT / 2);
        }
        const newFloor = playerPos.y > (FLOOR_HEIGHT / 2) ? 2 : 1;
        if (newFloor !== currentFloor) {
          currentFloor = newFloor;
          updateFloorVisibility();
        }
      } else {
        if (!elevatorMoving) {
          playerPos.y = currentFloor === 1 ? 0 : FLOOR_HEIGHT;
        }
      }
    }

    const promptElem = document.getElementById("interact-prompt");
    function checkElevatorProximity() {
      const dist = Math.hypot(playerPos.x - 23.75, playerPos.z - 12.5);
      if (dist < 3.2 && !elevatorMoving) {
        promptElem.style.display = "block";
      } else {
        promptElem.style.display = "none";
      }
    }

    function updateCurrentRoomLocation() {
      const floor = currentFloor;
      const rooms = ROOM_DATA.filter(r => r.floor === floor);

      let found = null;
      for (const r of rooms) {
        if (playerPos.x >= r.x && playerPos.x <= r.x + r.w &&
            playerPos.z >= r.z && playerPos.z <= r.z + r.d) {
          found = r;
          break;
        }
      }

      const hudFloor = document.getElementById("hud-floor");
      const hudRoom = document.getElementById("hud-room");
      const miniFloor = document.getElementById("mini-floor-txt");

      hudFloor.textContent = `FLOOR ${floor}`;
      miniFloor.textContent = `Floor ${floor}`;

      if (found && found.id !== currentRoomId) {
        currentRoomId = found.id;
        hudRoom.textContent = `${found.id}: ${found.name}`;
        document.getElementById("loc-banner").classList.add("active-room");
        setTimeout(() => document.getElementById("loc-banner").classList.remove("active-room"), 1000);
        sound.playRoomDing();
        openRoomDrawer(found);
      } else if (!found) {
        hudRoom.textContent = "Corridor / Circulation Hallway";
      }
    }

    // --- 15. DYNAMIC SPRING-ARM CAMERA & WALL OCCLUSION FADING ---
    function updateCamera(delta) {
      if (isFirstPerson) {
        player.visible = false;
        const eyePos = playerPos.clone().add(new THREE.Vector3(0, 1.5, 0));
        camera.position.copy(eyePos);

        const lookTarget = eyePos.clone().add(
          new THREE.Vector3(
            Math.sin(playerRotY) * Math.cos(cameraPitch),
            Math.sin(cameraPitch),
            Math.cos(playerRotY) * Math.cos(cameraPitch)
          )
        );
        camera.lookAt(lookTarget);
        restoreAllOccludedWalls();
      } else {
        player.visible = true;
        const targetPos = playerPos.clone().add(new THREE.Vector3(0, 1.35, 0)); // Doctor shoulder/head

        // Desired camera position in open air
        const desiredDistance = camDistanceSetting;
        const camHeight = 1.9;

        const camDir = new THREE.Vector3(
          -Math.sin(playerRotY),
          Math.sin(cameraPitch) * 1.5 + (camHeight / desiredDistance),
          -Math.cos(playerRotY)
        ).normalize();

        const desiredCamPos = targetPos.clone().addScaledVector(camDir, desiredDistance);

        // Filter active floor wall meshes for camera collision
        const activeWallMeshes = allWallMeshes.filter(m => m.userData.floor === currentFloor);

        // SPRING-ARM CAMERA COLLISION (PULLS CAMERA INWARD WHEN A WALL IS BEHIND THE PLAYER)
        raycaster.set(targetPos, camDir);
        raycaster.far = desiredDistance + 0.2;
        const camIntersects = raycaster.intersectObjects(activeWallMeshes, false);

        let targetDist = desiredDistance;
        if (camIntersects.length > 0) {
          // A wall is behind the camera: smoothly pull camera inward
          targetDist = Math.max(1.1, camIntersects[0].distance - 0.25);
        }

        // Smooth camera distance interpolation (lerp)
        currentCameraDistance += (targetDist - currentCameraDistance) * Math.min(1.0, (delta || 0.016) * 12);
        camera.position.copy(targetPos).addScaledVector(camDir, currentCameraDistance);
        camera.lookAt(targetPos.x, targetPos.y + 0.1, targetPos.z);

        // WALL OCCLUSION TRANSPARENCY (SEE-THROUGH WALLS BETWEEN CAMERA & DOCTOR)
        handleWallOcclusionFading(targetPos, activeWallMeshes);
      }
    }

    function handleWallOcclusionFading(targetPos, activeWallMeshes) {
      const camToTarget = targetPos.clone().sub(camera.position);
      const dist = camToTarget.length();
      if (dist < 0.1) return;

      const dir = camToTarget.clone().normalize();
      raycaster.set(camera.position, dir);
      raycaster.far = dist - 0.35; // Stop just before player

      const hits = raycaster.intersectObjects(activeWallMeshes, false);
      const currentlyHit = new Set();

      for (let i = 0; i < hits.length; i++) {
        const mesh = hits[i].object;
        currentlyHit.add(mesh);

        // Fade occluding wall so doctor is 100% visible
        if (mesh.material) {
          mesh.material.transparent = true;
          mesh.material.opacity = 0.20;
          mesh.material.depthWrite = false;
        }
      }

      // Restore walls that are no longer occluding
      occludedWallMeshes.forEach(mesh => {
        if (!currentlyHit.has(mesh) && mesh.material) {
          mesh.material.opacity = 1.0;
          mesh.material.transparent = false;
          mesh.material.depthWrite = true;
        }
      });

      occludedWallMeshes = currentlyHit;
    }

    function restoreAllOccludedWalls() {
      occludedWallMeshes.forEach(mesh => {
        if (mesh.material) {
          mesh.material.opacity = 1.0;
          mesh.material.transparent = false;
          mesh.material.depthWrite = true;
        }
      });
      occludedWallMeshes.clear();
    }

    function updateFloorVisibility() {
      if (viewFilter === "both") {
        floor1Group.visible = true;
        floor2Group.visible = true;
      } else if (viewFilter === "f1") {
        floor1Group.visible = true;
        floor2Group.visible = false;
      } else if (viewFilter === "f2") {
        floor1Group.visible = false;
        floor2Group.visible = true;
      } else {
        // "active" view
        if (currentFloor === 1) {
          floor1Group.visible = true;
          floor2Group.visible = isFirstPerson;
        } else {
          floor1Group.visible = true;
          floor2Group.visible = true;
        }
      }
      labelsGroup.visible = labelsVisible;
    }

    // --- 16. MINIMAP RADAR ---
    const miniCanvas = document.getElementById("minimap-canvas");
    const miniCtx = miniCanvas.getContext("2d");

    function drawMinimap() {
      miniCtx.clearRect(0, 0, miniCanvas.width, miniCanvas.height);

      const scaleX = miniCanvas.width / 44;
      const scaleZ = miniCanvas.height / 28;
      const ox = 2 * scaleX;
      const oz = 1.5 * scaleZ;

      const rooms = ROOM_DATA.filter(r => r.floor === currentFloor);
      rooms.forEach(r => {
        miniCtx.fillStyle = "#" + r.color.toString(16).padStart(6, '0') + "66";
        miniCtx.strokeStyle = "#38bdf888";
        miniCtx.lineWidth = 1;
        miniCtx.fillRect(ox + r.x * scaleX, oz + r.z * scaleZ, r.w * scaleX, r.d * scaleZ);
        miniCtx.strokeRect(ox + r.x * scaleX, oz + r.z * scaleZ, r.w * scaleX, r.d * scaleZ);

        miniCtx.fillStyle = "#ffffff";
        miniCtx.font = "bold 8px monospace";
        miniCtx.fillText(r.id, ox + (r.x + r.w / 2) * scaleX - 7, oz + (r.z + r.d / 2) * scaleZ + 3);
      });

      const px = ox + playerPos.x * scaleX;
      const pz = oz + playerPos.z * scaleZ;

      miniCtx.save();
      miniCtx.translate(px, pz);
      miniCtx.rotate(playerRotY);

      miniCtx.fillStyle = "rgba(56, 189, 248, 0.4)";
      miniCtx.beginPath();
      miniCtx.moveTo(0, 0);
      miniCtx.lineTo(-8, 16);
      miniCtx.lineTo(8, 16);
      miniCtx.closePath();
      miniCtx.fill();

      miniCtx.fillStyle = "#38bdf8";
      miniCtx.beginPath();
      miniCtx.arc(0, 0, 4.5, 0, Math.PI * 2);
      miniCtx.fill();
      miniCtx.strokeStyle = "#ffffff";
      miniCtx.lineWidth = 1.5;
      miniCtx.stroke();

      miniCtx.restore();
    }

    // --- 17. ELEVATOR ANIMATION ---
    function triggerElevator(targetFloor) {
      if (targetFloor === currentFloor || elevatorMoving) return;
      elevatorMoving = true;
      document.getElementById("elevator-modal").classList.remove("open");

      playerPos.x = 23.75;
      playerPos.z = 12.5;
      sound.playElevatorChime();

      const startY = currentFloor === 1 ? 0 : FLOOR_HEIGHT;
      const targetY = targetFloor === 1 ? 0 : FLOOR_HEIGHT;
      const startTime = performance.now();
      const duration = 2500;

      function animateElev(now) {
        const elapsed = now - startTime;
        const progress = Math.min(1, elapsed / duration);
        const ease = 0.5 - Math.cos(progress * Math.PI) / 2;

        playerPos.y = startY + (targetY - startY) * ease;
        elevatorCabin.position.y = playerPos.y;

        if (progress < 1) {
          requestAnimationFrame(animateElev);
        } else {
          currentFloor = targetFloor;
          playerPos.y = targetY;
          elevatorMoving = false;
          sound.playElevatorChime();
          updateFloorVisibility();
          updateElevatorButtons();
        }
      }
      requestAnimationFrame(animateElev);
    }

    function updateElevatorButtons() {
      document.getElementById("elev-btn-f1").classList.toggle("current", currentFloor === 1);
      document.getElementById("elev-btn-f2").classList.toggle("current", currentFloor === 2);
    }


    // =========================================================================
    // --- 20. ROUTE LINE DRAWING & HOLD-TO-FOLLOW ENGINE ---
    // =========================================================================
    let activeRoutePath = [];
    let activeRouteIndex = 0;
    let activeRouteTargetRoom = null;
    let isHoldingFollow = false;
    let routeGpsGroup = new THREE.Group();
    let routeLineMesh = null;
    let routeBeaconRing = null;

    // Distinct Doorway and Room Waypoints for all 26 Rooms
    const ROOM_NAV_WAYPOINTS = {
      // FIRST FLOOR
      "101": { door: new THREE.Vector3(6.0, 0, 18.0), inside: new THREE.Vector3(3.5, 0, 22.0) },
      "102": { door: new THREE.Vector3(9.3, 0, 18.0), inside: new THREE.Vector3(10.0, 0, 22.0) },
      "103": { door: new THREE.Vector3(15.2, 0, 18.0), inside: new THREE.Vector3(16.0, 0, 22.0) },
      "104": { door: new THREE.Vector3(20.9, 0, 18.0), inside: new THREE.Vector3(21.5, 0, 22.0) },
      "105": { door: new THREE.Vector3(25.9, 0, 18.0), inside: new THREE.Vector3(26.5, 0, 22.0) },
      "106": { door: new THREE.Vector3(31.2, 0, 18.0), inside: new THREE.Vector3(31.7, 0, 22.0) },
      "107": { door: new THREE.Vector3(36.8, 0, 18.0), inside: new THREE.Vector3(37.2, 0, 22.0) },
      "108": { door: new THREE.Vector3(12.0, 0, 14.5), inside: new THREE.Vector3(5.5, 0, 14.5) },
      "109": { door: new THREE.Vector3(12.0, 0, 10.1), inside: new THREE.Vector3(5.5, 0, 10.1) },
      "110": { door: new THREE.Vector3(27.2, 0, 14.5), inside: new THREE.Vector3(34.5, 0, 14.5) },
      "111": { door: new THREE.Vector3(27.2, 0, 10.1), inside: new THREE.Vector3(34.5, 0, 10.1) },
      "112": { door: new THREE.Vector3(5.2, 0, 7.0), inside: new THREE.Vector3(3.5, 0, 3.0) },
      "113": { door: new THREE.Vector3(12.3, 0, 7.0), inside: new THREE.Vector3(12.0, 0, 3.0) },
      "114": { door: new THREE.Vector3(18.2, 0, 7.0), inside: new THREE.Vector3(20.0, 0, 3.0) },
      "115": { door: new THREE.Vector3(23.6, 0, 7.0), inside: new THREE.Vector3(26.0, 0, 3.0) },
      "116": { door: new THREE.Vector3(29.6, 0, 7.0), inside: new THREE.Vector3(34.5, 0, 3.0) },

      // SECOND FLOOR
      "201": { door: new THREE.Vector3(6.0, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(3.5, FLOOR_HEIGHT, 22.0) },
      "202": { door: new THREE.Vector3(9.1, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(9.5, FLOOR_HEIGHT, 22.0) },
      "203": { door: new THREE.Vector3(14.8, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(15.5, FLOOR_HEIGHT, 22.0) },
      "204": { door: new THREE.Vector3(21.7, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(22.5, FLOOR_HEIGHT, 22.0) },
      "205": { door: new THREE.Vector3(28.2, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(29.0, FLOOR_HEIGHT, 22.0) },
      "206": { door: new THREE.Vector3(35.0, FLOOR_HEIGHT, 18.0), inside: new THREE.Vector3(36.0, FLOOR_HEIGHT, 22.0) },
      "207": { door: new THREE.Vector3(12.0, FLOOR_HEIGHT, 15.8), inside: new THREE.Vector3(5.5, FLOOR_HEIGHT, 15.5) },
      "208": { door: new THREE.Vector3(12.0, FLOOR_HEIGHT, 12.8), inside: new THREE.Vector3(5.5, FLOOR_HEIGHT, 12.5) },
      "209": { door: new THREE.Vector3(12.0, FLOOR_HEIGHT, 9.8), inside: new THREE.Vector3(5.5, FLOOR_HEIGHT, 9.5) },
      "210": { door: new THREE.Vector3(27.2, FLOOR_HEIGHT, 14.5), inside: new THREE.Vector3(34.5, FLOOR_HEIGHT, 14.5) },
      "211": { door: new THREE.Vector3(27.2, FLOOR_HEIGHT, 10.1), inside: new THREE.Vector3(34.5, FLOOR_HEIGHT, 10.1) },
      "212": { door: new THREE.Vector3(6.1, FLOOR_HEIGHT, 7.0), inside: new THREE.Vector3(4.5, FLOOR_HEIGHT, 3.0) },
      "213": { door: new THREE.Vector3(12.1, FLOOR_HEIGHT, 7.0), inside: new THREE.Vector3(12.5, FLOOR_HEIGHT, 3.0) },
      "214": { door: new THREE.Vector3(18.1, FLOOR_HEIGHT, 7.0), inside: new THREE.Vector3(19.0, FLOOR_HEIGHT, 3.0) },
      "215": { door: new THREE.Vector3(24.1, FLOOR_HEIGHT, 7.0), inside: new THREE.Vector3(25.0, FLOOR_HEIGHT, 3.0) },
      "216": { door: new THREE.Vector3(31.6, FLOOR_HEIGHT, 7.0), inside: new THREE.Vector3(34.0, FLOOR_HEIGHT, 3.0) },
    };

    function calculateHospitalPath(startPos, targetRoom) {
      const waypoints = [];
      const startFloor = startPos.y > (FLOOR_HEIGHT / 2) ? 2 : 1;
      const targetFloor = targetRoom.floor;
      const navInfo = ROOM_NAV_WAYPOINTS[targetRoom.id] || {
        door: new THREE.Vector3(targetRoom.x + targetRoom.w / 2, (targetFloor - 1) * FLOOR_HEIGHT, targetRoom.z + targetRoom.d / 2),
        inside: new THREE.Vector3(targetRoom.x + targetRoom.w / 2, (targetFloor - 1) * FLOOR_HEIGHT, targetRoom.z + targetRoom.d / 2)
      };

      waypoints.push(startPos.clone());

      // 1. Move to nearest corridor line on current floor
      const curY = (startFloor - 1) * FLOOR_HEIGHT;
      let curZ = startPos.z <= 12.5 ? 7.0 : 18.0;
      let curX = startPos.x;

      curX = Math.max(3.5, Math.min(36.5, curX));
      waypoints.push(new THREE.Vector3(curX, curY, curZ));

      // 2. Floor Transition via Dog-leg Stairs if floors differ
      if (startFloor !== targetFloor) {
        if (startFloor === 1 && targetFloor === 2) {
          // Walk to Flight 1 base
          waypoints.push(new THREE.Vector3(14.1, 0, 7.0));
          waypoints.push(new THREE.Vector3(14.1, 0.08, 8.2));
          // Climb Flight 1 to Half-Landing
          waypoints.push(new THREE.Vector3(14.1, 1.8, 14.5));
          waypoints.push(new THREE.Vector3(15.2, 1.8, 15.4));
          waypoints.push(new THREE.Vector3(16.3, 1.8, 14.5));
          // Climb Flight 2 to Floor 2
          waypoints.push(new THREE.Vector3(16.3, FLOOR_HEIGHT, 8.2));
          waypoints.push(new THREE.Vector3(16.3, FLOOR_HEIGHT, 7.0));
          curX = 16.3;
          curZ = 7.0;
        } else {
          // Floor 2 down to Floor 1
          waypoints.push(new THREE.Vector3(16.3, FLOOR_HEIGHT, 7.0));
          waypoints.push(new THREE.Vector3(16.3, FLOOR_HEIGHT, 8.2));
          waypoints.push(new THREE.Vector3(16.3, 1.8, 14.5));
          waypoints.push(new THREE.Vector3(15.2, 1.8, 15.4));
          waypoints.push(new THREE.Vector3(14.1, 1.8, 14.5));
          waypoints.push(new THREE.Vector3(14.1, 0.08, 8.2));
          waypoints.push(new THREE.Vector3(14.1, 0, 7.0));
          curX = 14.1;
          curZ = 7.0;
        }
      }

      // 3. Navigate on Target Floor to Destination Doorway
      const destY = (targetFloor - 1) * FLOOR_HEIGHT;
      const targetDoor = navInfo.door;
      const targetCorridorZ = targetDoor.z <= 12.5 ? 7.0 : 18.0;

      if (Math.abs(curZ - targetCorridorZ) > 3.0) {
        let crossX = 19.75;
        if (targetDoor.x < 15.0) crossX = 12.0;
        else if (targetDoor.x > 25.0) crossX = 27.25;

        waypoints.push(new THREE.Vector3(crossX, destY, curZ));
        waypoints.push(new THREE.Vector3(crossX, destY, targetCorridorZ));
        curX = crossX;
        curZ = targetCorridorZ;
      }

      // Along corridor to doorway
      waypoints.push(new THREE.Vector3(targetDoor.x, destY, curZ));
      waypoints.push(new THREE.Vector3(targetDoor.x, destY, targetDoor.z));

      // Finally step into the room interior
      waypoints.push(navInfo.inside.clone());

      return waypoints;
    }

    // DRAW THE GLOWING MAP LINE FROM CHARACTER TO DESTINATION
    function setRouteToDestination(targetRoom) {
      if (!targetRoom) return;
      activeRouteTargetRoom = targetRoom;

      // 1. Calculate path waypoints from character to destination
      activeRoutePath = calculateHospitalPath(playerPos, targetRoom);
      activeRouteIndex = 1;

      // 2. Turn doctor and camera towards the route immediately!
      if (activeRoutePath.length > 1) {
        const dx = activeRoutePath[1].x - playerPos.x;
        const dz = activeRoutePath[1].z - playerPos.z;
        if (Math.hypot(dx, dz) > 0.05) {
          playerRotY = Math.atan2(dx, dz);
          player.rotation.y = playerRotY;
        }
      }
      cameraPitch = 0.18;
      updateCamera(0.016);

      // 3. Render glowing 3D map line on floor (elevated above floor slab)
      renderRouteMapLine();

      // 4. Close directory modal
      closeDirectoryModal();

      // 5. Open the on-screen "HOLD TO FOLLOW LINE" controller
      const hud = document.getElementById("route-follower-hud");
      const badge = document.getElementById("route-dest-id");
      const title = document.getElementById("route-dest-title");
      const catInfo = CAT_COLORS[targetRoom.cat] || { css: "#0284c7" };

      badge.textContent = targetRoom.id;
      badge.style.background = catInfo.css;
      title.textContent = `${targetRoom.name} (Floor ${targetRoom.floor})`;
      updateRouteRemainingDistance();

      hud.classList.add("active");
      sound.playElevatorChime();
    }

    // HELPER TO GET TRUE FLOOR SURFACE ELEVATION (FLOOR SLAB IS AT Y = 0.25 - 0.29m)
    function getFloorSurfaceY(y) {
      if (y >= FLOOR_HEIGHT - 0.2) {
        return FLOOR_HEIGHT + 0.30; // Floor 2 surface (3.90m)
      } else if (y <= 0.2) {
        return 0.30; // Floor 1 surface (0.30m)
      } else {
        // Stairs transition
        return y + 0.22;
      }
    }

    // CREATE A HIGH-VISIBILITY 3D GLOWING GPS FLOOR RIBBON (0.35m WIDE)
    function renderRouteMapLine() {
      while (routeGpsGroup.children.length > 0) {
        routeGpsGroup.remove(routeGpsGroup.children[0]);
      }

      if (!activeRoutePath || activeRoutePath.length < 2) return;

      // Current player position elevated to surface
      const curY = getFloorSurfaceY(playerPos.y);
      const displayPts = [new THREE.Vector3(playerPos.x, curY, playerPos.z)];

      for (let i = activeRouteIndex; i < activeRoutePath.length; i++) {
        const p = activeRoutePath[i];
        displayPts.push(new THREE.Vector3(p.x, getFloorSurfaceY(p.y), p.z));
      }

      if (displayPts.length < 2) return;

      // 1. Build a 3D Flat Ribbon Mesh (0.36m wide tape on floor)
      const ribbonGeo = new THREE.BufferGeometry();
      const vertices = [];
      const uvs = [];
      const halfWidth = 0.18; // 0.36m total width

      for (let i = 0; i < displayPts.length; i++) {
        const p = displayPts[i];
        let dir = new THREE.Vector3(0, 0, 1);
        if (i < displayPts.length - 1) {
          dir.subVectors(displayPts[i + 1], p).normalize();
        } else if (i > 0) {
          dir.subVectors(p, displayPts[i - 1]).normalize();
        }

        // Perpendicular vector on floor
        const perp = new THREE.Vector3(-dir.z, 0, dir.x).normalize().multiplyScalar(halfWidth);

        // Left and Right vertex
        vertices.push(p.x - perp.x, p.y + 0.01, p.z - perp.z);
        vertices.push(p.x + perp.x, p.y + 0.01, p.z + perp.z);
        uvs.push(0, i / (displayPts.length - 1));
        uvs.push(1, i / (displayPts.length - 1));
      }

      const indices = [];
      for (let i = 0; i < displayPts.length - 1; i++) {
        const base = i * 2;
        indices.push(base, base + 1, base + 2);
        indices.push(base + 1, base + 3, base + 2);
      }

      ribbonGeo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      ribbonGeo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
      ribbonGeo.setIndex(indices);
      ribbonGeo.computeVertexNormals();

      const ribbonMat = new THREE.MeshBasicMaterial({
        color: 0x06b6d4, // Bright neon cyan
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.88,
        depthWrite: false
      });
      const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
      routeGpsGroup.add(ribbonMesh);

      // 2. High-contrast center spine line (elevated slightly above ribbon)
      const spineGeo = new THREE.BufferGeometry().setFromPoints(displayPts.map(p => new THREE.Vector3(p.x, p.y + 0.02, p.z)));
      const spineMat = new THREE.LineBasicMaterial({
        color: 0xffffff,
        linewidth: 3,
        transparent: true,
        opacity: 0.95
      });
      const spineLine = new THREE.Line(spineGeo, spineMat);
      routeGpsGroup.add(spineLine);

      // 3. Glowing circular waypoint beacons along the path
      const dotGeo = new THREE.CylinderGeometry(0.24, 0.24, 0.04, 16);
      const dotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
      for (let i = 1; i < displayPts.length - 1; i++) {
        const pt = displayPts[i];
        const dot = new THREE.Mesh(dotGeo, dotMat);
        dot.position.set(pt.x, pt.y + 0.015, pt.z);
        routeGpsGroup.add(dot);
      }

      // 4. Target Destination Glowing Beacon Ring (Emerald Green)
      const finalPt = activeRoutePath[activeRoutePath.length - 1];
      const finalY = getFloorSurfaceY(finalPt.y);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0x10b981,
        side: THREE.DoubleSide
      });
      routeBeaconRing = new THREE.Mesh(new THREE.RingGeometry(0.3, 0.7, 32), ringMat);
      routeBeaconRing.rotation.x = -Math.PI / 2;
      routeBeaconRing.position.set(finalPt.x, finalY + 0.03, finalPt.z);
      routeGpsGroup.add(routeBeaconRing);

      // Start position marker
      const startDot = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.05, 16), new THREE.MeshBasicMaterial({ color: 0x22c55e }));
      startDot.position.set(playerPos.x, curY + 0.015, playerPos.z);
      routeGpsGroup.add(startDot);

      scene.add(routeGpsGroup);
    }

    function updateRouteRemainingDistance() {
      if (!activeRoutePath || activeRouteIndex >= activeRoutePath.length) return;
      let totalDist = Math.hypot(activeRoutePath[activeRouteIndex].x - playerPos.x, activeRoutePath[activeRouteIndex].z - playerPos.z);
      for (let i = activeRouteIndex; i < activeRoutePath.length - 1; i++) {
        totalDist += activeRoutePath[i].distanceTo(activeRoutePath[i + 1]);
      }
      document.getElementById("route-dist-txt").textContent = `Remaining: ${totalDist.toFixed(1)}m`;
    }

    function clearActiveRoute() {
      activeRoutePath = [];
      activeRouteIndex = 0;
      activeRouteTargetRoom = null;
      isHoldingFollow = false;
      while (routeGpsGroup.children.length > 0) {
        routeGpsGroup.remove(routeGpsGroup.children[0]);
      }
      scene.remove(routeGpsGroup);

      const hud = document.getElementById("route-follower-hud");
      hud.classList.remove("active");
      document.querySelector(".controls-hud").style.display = "flex";
    }

    // PROCESS ROUTE UPDATES & LINE FOLLOWING
    function processFollowRoute(delta) {
      if (!activeRoutePath || activeRoutePath.length === 0) return;

      // 1. Pulse target beacon ring
      if (routeBeaconRing) {
        const s = 1.0 + Math.sin(performance.now() * 0.007) * 0.15;
        routeBeaconRing.scale.set(s, s, s);
      }

      const holdBtn = document.getElementById("btn-hold-follow");
      if (holdBtn) holdBtn.classList.toggle("pressing", isHoldingFollow);

      // Check distance to final destination target
      const finalPt = activeRoutePath[activeRoutePath.length - 1];
      const distToFinal = Math.hypot(finalPt.x - playerPos.x, finalPt.z - playerPos.z);
      if (distToFinal < 1.6 && Math.abs(playerPos.y - finalPt.y) < 1.0) {
        reachDestination();
        return;
      }

      if (isHoldingFollow) {
        // --- AUTO-FOLLOWING MODE (BUTTON IS HELD) ---
        const targetPt = activeRoutePath[activeRouteIndex];
        if (!targetPt) {
          reachDestination();
          return;
        }

        const dx = targetPt.x - playerPos.x;
        const dz = targetPt.z - playerPos.z;
        const dist2D = Math.hypot(dx, dz);

        // Turn smoothly towards the next waypoint
        if (dist2D > 0.08) {
          const targetRotY = Math.atan2(dx, dz);
          let diff = targetRotY - playerRotY;
          while (diff < -Math.PI) diff += Math.PI * 2;
          while (diff > Math.PI) diff -= Math.PI * 2;
          playerRotY += diff * Math.min(1.0, delta * 10);
        }

        const moveSpeed = 4.8;
        const step = moveSpeed * delta;

        if (dist2D <= step) {
          playerPos.x = targetPt.x;
          playerPos.z = targetPt.z;
          playerPos.y = targetPt.y;
          activeRouteIndex++;

          const newFloor = playerPos.y > (FLOOR_HEIGHT / 2) ? 2 : 1;
          if (newFloor !== currentFloor) {
            currentFloor = newFloor;
            updateFloorVisibility();
          }

          renderRouteMapLine();
          updateRouteRemainingDistance();

          if (activeRouteIndex >= activeRoutePath.length) {
            reachDestination();
            return;
          }
        } else {
          const nx = dx / dist2D;
          const nz = dz / dist2D;
          playerPos.x += nx * step;
          playerPos.z += nz * step;
          playerPos.y += (targetPt.y - playerPos.y) * Math.min(1.0, delta * 9);
        }

        // Animate walking limbs
        walkCycle += delta * 12;
        playerLegL.rotation.x = Math.sin(walkCycle) * 0.6;
        playerLegR.rotation.x = -Math.sin(walkCycle) * 0.6;
        playerArmL.rotation.x = -Math.sin(walkCycle) * 0.5;
        playerArmR.rotation.x = Math.sin(walkCycle) * 0.5;
        playerBody.position.y = 0.95 + Math.abs(Math.sin(walkCycle)) * 0.04;

        stepSoundTimer += delta;
        if (stepSoundTimer > 0.28) {
          sound.playFootstep();
          stepSoundTimer = 0;
        }

        player.position.copy(playerPos);
        player.rotation.y = playerRotY;
        updateCurrentRoomLocation();
        updateCamera(delta);
      } else {
        // --- FREE MOVEMENT MODE (USER CAN FREELY WALK WITH WASD AND LOOK AROUND) ---
        updatePlayerMovement(delta);

        // Dynamically advance activeRouteIndex if player walks close to the next waypoint freely!
        if (activeRouteIndex < activeRoutePath.length) {
          const nextPt = activeRoutePath[activeRouteIndex];
          const dToNext = Math.hypot(nextPt.x - playerPos.x, nextPt.z - playerPos.z);
          if (dToNext < 1.2 && Math.abs(playerPos.y - nextPt.y) < 1.0) {
            activeRouteIndex++;
            renderRouteMapLine();
            updateRouteRemainingDistance();
          }
        }
      }
    }

    function reachDestination() {
      const reachedRoom = activeRouteTargetRoom;
      clearActiveRoute();
      sound.playRoomDing();
      if (reachedRoom) {
        openRoomDrawer(reachedRoom);
      }
    }

    // =========================================================================
    let currentFilterCategory = "all";

    function populateDirectoryGrid() {
      const grid = document.getElementById("dir-room-grid");
      grid.innerHTML = "";

      const query = (document.getElementById("dir-search-input").value || "").toLowerCase().trim();

      // Filter rooms
      const filtered = ROOM_DATA.filter(r => {
        if (r.id.includes("Lobby") || r.id.includes("Stairs") || r.id.includes("Elevator")) return false;

        // Category / Floor filter
        if (currentFilterCategory === "f1" && r.floor !== 1) return false;
        if (currentFilterCategory === "f2" && r.floor !== 2) return false;
        if (currentFilterCategory !== "all" && currentFilterCategory !== "f1" && currentFilterCategory !== "f2") {
          if (r.cat !== currentFilterCategory) return false;
        }

        // Search text filter
        if (query.length > 0) {
          const matchId = r.id.toLowerCase().includes(query);
          const matchName = r.name.toLowerCase().includes(query);
          const matchCat = r.cat.toLowerCase().includes(query);
          const matchBeds = (r.beds || "").toLowerCase().includes(query);
          if (!matchId && !matchName && !matchCat && !matchBeds) return false;
        }

        return true;
      });

      if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #94a3b8;">
          <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
          <div style="font-size: 15px; font-weight: 700; color: #fff;">No departments found matching "${query}"</div>
          <div style="font-size: 12px; margin-top: 4px;">Try searching for "ICU", "Ward", "101", "Cafeteria", or "Doctor"</div>
        </div>`;
        return;
      }

      filtered.forEach(room => {
        const catInfo = CAT_COLORS[room.cat] || { css: "#0284c7" };
        const card = document.createElement("div");
        card.className = "room-dir-card";

        card.innerHTML = `
          <div class="card-top">
            <span class="card-id-pill" style="background: ${catInfo.css};">${room.id}</span>
            <span class="card-floor-tag">Floor ${room.floor}</span>
          </div>
          <div class="card-title">${room.name}</div>
          <div class="card-sub">
            <span style="color:${catInfo.css}">●</span> ${room.cat} • ${room.beds || "Active Care"}
          </div>
          <button class="btn-card-route" data-select-room="${room.id}">
            <span>🗺️</span> Draw Route Line to Destination
          </button>
        `;

        // Clicking the button or tapping the card draws the route line
        const routeBtn = card.querySelector("[data-select-room]");
        const chooseRoom = (e) => {
          if (e) {
            e.preventDefault();
            e.stopPropagation();
          }
          setRouteToDestination(room);
        };

        routeBtn.addEventListener("click", chooseRoom);
        routeBtn.addEventListener("touchend", chooseRoom);

        card.style.cursor = "pointer";
        card.addEventListener("click", chooseRoom);

        grid.appendChild(card);
      });
    }

    function openDirectoryModal() {
      populateDirectoryGrid();
      const backdrop = document.getElementById("dir-modal-backdrop");
      backdrop.classList.add("open");
      const isMobile = window.innerWidth <= 768 || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
      if (!isMobile) {
        document.getElementById("dir-search-input").focus();
      }
    }

    function closeDirectoryModal() {
      const backdrop = document.getElementById("dir-modal-backdrop");
      backdrop.classList.remove("open");
      document.getElementById("dir-search-input").blur();
    }

    // --- 18. EVENTS & UI ---
    function setupEvents() {
      window.addEventListener("keydown", (e) => {
        sound.init();
        const k = e.key.toLowerCase();
        if (k === "w" || e.key === "ArrowUp") keys.w = true;
        if (k === "s" || e.key === "ArrowDown") keys.s = true;
        if (k === "a" || e.key === "ArrowLeft") keys.a = true;
        if (k === "d" || e.key === "ArrowRight") keys.d = true;
        if (e.key === "Shift") keys.shift = true;
        if (k === "v") toggleCameraView();
        if (k === "l") toggleWallLabels();
        if (k === "p") toggleDrawingMode();
        if (k === "e") handleInteractionKey();
        if (k === "escape") {
          clearActiveRoute();
          closeDirectoryModal();
        }
        if (k === "/" || k === "f") {
          e.preventDefault();
          openDirectoryModal();
        }
        // Cancel auto-walk if manual movement keys are pressed
        if (isAutoNavigating && (k === "w" || k === "a" || k === "s" || k === "d")) {
          clearActiveRoute();
        }

      });

      window.addEventListener("keyup", (e) => {
        const k = e.key.toLowerCase();
        if (k === "w" || e.key === "ArrowUp") keys.w = false;
        if (k === "s" || e.key === "ArrowDown") keys.s = false;
        if (k === "a" || e.key === "ArrowLeft") keys.a = false;
        if (k === "d" || e.key === "ArrowRight") keys.d = false;
        if (e.key === "Shift") keys.shift = false;
      });

      renderer.domElement.addEventListener("mousedown", (e) => {
        sound.init();
        if (isDrawMode && e.button === 0) {
          // Left click draws on floor
          isDrawingMouseActive = true;
          const hit = getFloorIntersection(e.clientX, e.clientY);
          if (hit) addDrawnPoint(hit);
          return;
        }
        if (isGameMode) {
          mouseDrag = true;
          prevMouseX = e.clientX;
          prevMouseY = e.clientY;
        }
      });

      window.addEventListener("mouseup", () => { mouseDrag = false; isDrawingMouseActive = false; });

      window.addEventListener("mousemove", (e) => {
        if (isDrawMode) {
          const hit = getFloorIntersection(e.clientX, e.clientY);
          if (hit && drawCursorRing) {
            drawCursorRing.position.copy(hit);
            drawCursorRing.position.y += 0.01;
            drawCursorRing.visible = true;
            if (isDrawingMouseActive) {
              addDrawnPoint(hit);
            }
          }
          return;
        }
        if (mouseDrag && isGameMode) {
          const dx = e.clientX - prevMouseX;
          const dy = e.clientY - prevMouseY;
          prevMouseX = e.clientX;
          prevMouseY = e.clientY;

          playerRotY -= dx * 0.006;
          cameraPitch = Math.max(-0.4, Math.min(0.75, cameraPitch + dy * 0.005));
        }
      });

      const attachDpad = (id, keyName) => {
        const btn = document.getElementById(id);
        btn.addEventListener("mousedown", () => { sound.init(); keys[keyName] = true; });
        btn.addEventListener("mouseup", () => keys[keyName] = false);
        btn.addEventListener("touchstart", (e) => { e.preventDefault(); sound.init(); keys[keyName] = true; });
        btn.addEventListener("touchend", () => keys[keyName] = false);
      };
      attachDpad("btn-dpad-up", "w");
      attachDpad("btn-dpad-down", "s");
      attachDpad("btn-dpad-left", "a");
      attachDpad("btn-dpad-right", "d");
      document.getElementById("btn-dpad-action").addEventListener("click", () => handleInteractionKey());

      window.addEventListener("resize", onWindowResize);
    }

    function toggleCameraView() {
      isFirstPerson = !isFirstPerson;
      document.getElementById("btn-view-toggle").innerHTML = `<span>👁️</span> ${isFirstPerson ? "1st Person" : "3rd Person"}`;
      updateFloorVisibility();
    }

    function toggleWallLabels() {
      labelsVisible = !labelsVisible;
      labelsGroup.visible = labelsVisible;
      const txt = labelsVisible ? "ON" : "OFF";
      const btn1 = document.getElementById("btn-labels-toggle");
      if (btn1) {
        btn1.innerHTML = `<span>🏷️</span> Wall Labels: ${txt}`;
        btn1.classList.toggle("active", labelsVisible);
      }
      const btn2 = document.getElementById("btn-dock-labels");
      if (btn2) {
        btn2.innerHTML = `<span class="pill-icon">🏷️</span> Colored Wall Signs: ${txt}`;
        btn2.classList.toggle("active", labelsVisible);
      }
      const mBtn = document.getElementById("m-btn-labels");
      if (mBtn) mBtn.classList.toggle("active", labelsVisible);
    }

    function handleInteractionKey() {
      const distElev = Math.hypot(playerPos.x - 23.75, playerPos.z - 12.5);
      if (distElev < 3.2) {
        document.getElementById("elevator-modal").classList.toggle("open");
        updateElevatorButtons();
      }
    }

    function setupUI() {
      document.getElementById("btn-toggle-mode").addEventListener("click", toggleMode);
      document.getElementById("btn-mode-game").addEventListener("click", () => setMode(true));
      document.getElementById("btn-mode-orbit").addEventListener("click", () => setMode(false));

      function toggleMode() { setMode(!isGameMode); }
      function setMode(game) {
        isGameMode = game;
        controls.enabled = !isGameMode;
        document.getElementById("btn-mode-game").classList.toggle("active", isGameMode);
        document.getElementById("btn-mode-orbit").classList.toggle("active", !isGameMode);
        document.getElementById("btn-toggle-mode").innerHTML = `<span>${isGameMode ? "🎮" : "🌐"}</span> ${isGameMode ? "Game Walkthrough Mode" : "Orbit Overview Mode"}`;

        if (!isGameMode) {
          camera.position.set(20, 38, -32);
          controls.target.set(20, 2, 12.5);
          controls.update();
          restoreAllOccludedWalls();
        }
      }

      document.getElementById("btn-view-toggle").addEventListener("click", toggleCameraView);

      // DRAWING SYSTEM LISTENERS
      document.getElementById("btn-toggle-draw").addEventListener("click", () => toggleDrawingMode());
      document.getElementById("btn-close-draw").addEventListener("click", () => toggleDrawingMode(false));
      document.getElementById("btn-undo-draw").addEventListener("click", undoLastDrawnPoint);
      document.getElementById("btn-clear-draw").addEventListener("click", clearDrawnLine);
      document.getElementById("btn-walk-drawn-path").addEventListener("click", walkDrawnPath);

      // Color swatch clicks
      document.querySelectorAll(".color-swatch").forEach(swatch => {
        swatch.addEventListener("click", function() {
          document.querySelectorAll(".color-swatch").forEach(s => s.classList.remove("active"));
          this.classList.add("active");
          drawnLineColor = parseInt(this.dataset.color);
          if (drawCursorRing) drawCursorRing.material.color.setHex(drawnLineColor);
          updateDrawnLineVisualization();
        });
      });

      document.getElementById("btn-labels-toggle").addEventListener("click", toggleWallLabels);
      document.getElementById("btn-dock-labels").addEventListener("click", toggleWallLabels);

      // Camera distance cycle (Close / Medium / Wide)
      document.getElementById("btn-dock-cam-dist").addEventListener("click", function() {
        if (camDistanceSetting === 3.6) {
          camDistanceSetting = 4.8;
          this.innerHTML = `<span class="pill-icon">🎥</span> Cam Distance: Wide`;
        } else if (camDistanceSetting === 4.8) {
          camDistanceSetting = 2.4;
          this.innerHTML = `<span class="pill-icon">🎥</span> Cam Distance: Close`;
        } else {
          camDistanceSetting = 3.6;
          this.innerHTML = `<span class="pill-icon">🎥</span> Cam Distance: Medium`;
        }
      });

      document.getElementById("btn-sound-toggle").addEventListener("click", function() {
        sound.init();
        sound.enabled = !sound.enabled;
        this.innerHTML = `<span>${sound.enabled ? "🔊" : "🔇"}</span> Sound: ${sound.enabled ? "On" : "Off"}`;
      });

      const floorBtns = [
        { id: "btn-floor-active", mode: "active" },
        { id: "btn-floor-both", mode: "both" },
        { id: "btn-floor-f1", mode: "f1" },
        { id: "btn-floor-f2", mode: "f2" }
      ];

      floorBtns.forEach(item => {
        document.getElementById(item.id).addEventListener("click", () => {
          floorBtns.forEach(b => document.getElementById(b.id).classList.remove("active"));
          document.getElementById(item.id).classList.add("active");
          viewFilter = item.mode;
          updateFloorVisibility();
        });
      });

      document.getElementById("elev-btn-f1").addEventListener("click", () => triggerElevator(1));
      document.getElementById("elev-btn-f2").addEventListener("click", () => triggerElevator(2));
      document.getElementById("elev-close-btn").addEventListener("click", () => {
        document.getElementById("elevator-modal").classList.remove("open");
      });

      document.querySelectorAll("[data-teleport]").forEach(btn => {
        btn.addEventListener("click", () => {
          const roomId = btn.dataset.teleport;
          const r = ROOM_DATA.find(item => item.id === roomId);
          if (r) {
            currentFloor = r.floor;
            playerPos.set(r.x + r.w / 2, (r.floor - 1) * FLOOR_HEIGHT, r.z + r.d / 2);
            updateElevatorButtons();
            updateFloorVisibility();
            openRoomDrawer(r);
          }
        });
      });


      // DIRECTORY & SEARCH MODAL LISTENERS
      document.getElementById("btn-open-directory").addEventListener("click", openDirectoryModal);
      document.getElementById("close-dir-modal").addEventListener("click", closeDirectoryModal);
      document.getElementById("dir-modal-backdrop").addEventListener("click", (e) => {
        if (e.target.id === "dir-modal-backdrop") {
          closeDirectoryModal();
        }
      });

      // ROUTE FOLLOWER "HOLD TO FOLLOW LINE" CONTROLLER
      const holdBtn = document.getElementById("btn-hold-follow");
      const startHold = (e) => { 
        if (e.cancelable && e.type !== "mousedown") e.preventDefault(); 
        sound.init(); 
        isHoldingFollow = true; 
      };
      const stopHold = () => { 
        isHoldingFollow = false; 
      };

      holdBtn.addEventListener("mousedown", startHold);
      window.addEventListener("mouseup", stopHold);
      holdBtn.addEventListener("touchstart", startHold, { passive: false });
      holdBtn.addEventListener("touchend", stopHold);
      holdBtn.addEventListener("touchcancel", stopHold);
      window.addEventListener("blur", stopHold);

      document.getElementById("btn-clear-route").addEventListener("click", clearActiveRoute);

      document.getElementById("dir-search-input").addEventListener("input", populateDirectoryGrid);

      // Filter chips
      document.querySelectorAll(".filter-chip").forEach(chip => {
        chip.addEventListener("click", function() {
          document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
          this.classList.add("active");
          currentFilterCategory = this.dataset.filter;
          populateDirectoryGrid();
        });
      });

      // Display directory modal at starting point so users immediately see all rooms!
      setTimeout(openDirectoryModal, 800);

      document.getElementById("close-drawer").addEventListener("click", () => {
        document.getElementById("room-drawer").classList.remove("open");
      });
    }

    function openRoomDrawer(r) {
      document.getElementById("d-badge").textContent = `ROOM ${r.id}`;
      document.getElementById("d-title").textContent = r.name;
      document.getElementById("d-cat").textContent = r.cat;
      document.getElementById("d-floor").textContent = `${r.floor === 1 ? "1st" : "2nd"} Floor`;
      document.getElementById("d-size").textContent = `${r.w}m × ${r.d}m (${(r.w * r.d).toFixed(0)}m²)`;
      document.getElementById("d-beds").textContent = r.beds;
      document.getElementById("d-equipment").innerHTML = r.eq.split(", ").map(item => `• ${item}`).join("<br>");

      const dot = document.getElementById("d-dot");
      dot.style.background = "#" + r.color.toString(16).padStart(6, '0');

      document.getElementById("room-drawer").classList.add("open");
    }

    function onWindowResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // --- 19. MAIN ANIMATION LOOP ---
    let lastTime = performance.now();
    function animate() {
      requestAnimationFrame(animate);
      const now = performance.now();
      const delta = Math.min(0.08, (now - lastTime) / 1000);
      lastTime = now;

      if (activeRoutePath && activeRoutePath.length > 0) {
        processFollowRoute(delta);
      } else {
        updatePlayerMovement(delta);
      }

      if (!isGameMode) {
        controls.update();
      }

      drawMinimap();
      renderer.render(scene, camera);
    }

    window.addEventListener("DOMContentLoaded", init);
  </script>

  <!-- LIVE ROUTE & HOLD-TO-FOLLOW ON-SCREEN CONTROLLER -->
  <div class="route-follower-hud" id="route-follower-hud">
    <div class="route-info-box">
      <div class="route-dest-badge">
        <span class="route-dest-id" id="route-dest-id">101</span>
        <span class="route-dest-title" id="route-dest-title">Emergency Room</span>
      </div>
      <div class="route-dist-txt" id="route-dist-txt">Remaining: 24.5m</div>
    </div>

    <!-- HOLD BUTTON TO FOLLOW THE LINE -->
    <button class="btn-hold-follow" id="btn-hold-follow">
      <span class="follow-icon">🚶</span>
      <span>HOLD TO FOLLOW LINE</span>
      <span class="follow-sub">(or Hold W / Space)</span>
    </button>

    <button class="btn-clear-route" id="btn-clear-route" title="Clear Route Line">✕</button>
  </div>

  <!-- HOSPITAL DIRECTORY & SEARCH MODAL (DISPLAYS LIST OF ALL ROOMS AT START) -->
  <div class="directory-modal-backdrop" id="dir-modal-backdrop">
    <div class="directory-modal">
      <div class="dir-header">
        <div class="dir-title-area">
          <h2>🏥 Hospital Room Directory & GPS Navigation</h2>
          <p>Select any room or search to see route trail and auto-walk directly to your destination</p>
        </div>
        <button class="close-btn" id="close-dir-modal" style="font-size: 22px; width: 36px; height: 36px;">✕</button>
      </div>

      <div class="dir-search-bar">
        <div class="search-input-wrap">
          <span class="search-icon">🔍</span>
          <input type="text" id="dir-search-input" placeholder="Search room name, ID (e.g., ICU, 101, Ward, Cafeteria, OT, Maternity)..." autocomplete="off">
        </div>
      </div>

      <div class="dir-filters" id="dir-filter-chips">
        <div class="filter-chip active" data-filter="all">All Rooms (26)</div>
        <div class="filter-chip" data-filter="f1">Floor 1 (14)</div>
        <div class="filter-chip" data-filter="f2">Floor 2 (12)</div>
        <div class="filter-chip" data-filter="Emergency">🚨 Emergency</div>
        <div class="filter-chip" data-filter="Surgical">🔬 Surgery / ICU</div>
        <div class="filter-chip" data-filter="Wards">🛏️ Wards</div>
        <div class="filter-chip" data-filter="Diagnostics">🩺 Diagnostics</div>
        <div class="filter-chip" data-filter="Offices">💼 Doctors' Suites</div>
        <div class="filter-chip" data-filter="Facilities">☕ Facilities</div>
      </div>

      <div class="dir-body">
        <div class="dir-grid" id="dir-room-grid"></div>
      </div>
    </div>
  </div>


  <!-- DRAWING MODE FLOATING TOOLBAR HUD -->
  <div class="draw-toolbar-hud" id="draw-toolbar-hud">
    <div class="draw-tag">
      <span>✏️</span> Draw Mode
    </div>

    <!-- Color palette selector -->
    <div class="color-swatches" id="draw-swatches">
      <div class="color-swatch active" data-color="0x06b6d4" style="background:#06b6d4;" title="Neon Cyan"></div>
      <div class="color-swatch" data-color="0x10b981" style="background:#10b981;" title="Emerald Green"></div>
      <div class="color-swatch" data-color="0xf59e0b" style="background:#f59e0b;" title="Warm Amber"></div>
      <div class="color-swatch" data-color="0xf43f5e" style="background:#f43f5e;" title="Coral Red"></div>
      <div class="color-swatch" data-color="0xa855f7" style="background:#a855f7;" title="Purple"></div>
    </div>

    <div class="draw-dist-badge" id="draw-dist-txt">Length: 0.0m</div>

    <button class="btn-draw-action btn-draw-walk" id="btn-walk-drawn-path" disabled>
      <span>🚶</span> Walk This Path
    </button>
    <button class="btn-draw-action" id="btn-undo-draw">
      <span>↩️</span> Undo
    </button>
    <button class="btn-draw-action" id="btn-clear-draw">
      <span>🗑️</span> Clear
    </button>
    <button class="btn-draw-action" id="btn-close-draw" style="background:rgba(244,63,94,0.2); border-color:rgba(244,63,94,0.4); color:#fb7185;">
      <span>✕</span> Exit
    </button>
  </div>


  <!-- MOBILE FLOATING QUICK ACTIONS BAR -->
  <div class="mobile-floating-bar" id="mobile-floating-bar">
    <button class="m-btn" id="m-btn-search" title="Search Rooms">🔍</button>
    <button class="m-btn" id="m-btn-view" title="Toggle 1st/3rd Person">👁️</button>
    <button class="m-btn" id="m-btn-map" title="Toggle Minimap">🗺️</button>
    <button class="m-btn" id="m-btn-labels" title="Toggle Wall Labels">🏷️</button>
    <button class="m-btn" id="m-btn-menu" title="Menu / Filters">☰</button>
  </div>

  <!-- BACKDROP FOR MOBILE OFF-CANVAS MENU -->
  <div id="mobile-menu-backdrop"></div>

  <!-- VIRTUAL ANALOG TOUCH JOYSTICK (MOBILE MOVEMENT) -->
  <div class="virtual-joystick-zone" id="joystick-zone">
    <div class="joystick-base" id="joystick-base">
      <div class="joystick-stick" id="joystick-stick"></div>
    </div>
  </div>

</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("hospital_3d_viewer.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated index.html and hospital_3d_viewer.html successfully!")
