const INTENTS = ['attack','defend','buff'];
let state = null;

function initialState(){
  return {
    floor:1,
    player:{hp:60,maxHp:60,ase:3,block:0},
    enemy:{name:'Spirit Foe F1',hp:24,maxHp:24,strength:0,turn:0},
    hand:[
      {name:'Strike (Ogun)',cost:1,type:'Attack',desc:'Deal 6 damage.'},
      {name:'Strike (Ogun)',cost:1,type:'Attack',desc:'Deal 6 damage.'},
      {name:'Defend (Obatala)',cost:1,type:'Skill',desc:'Gain 5 Block.'},
      {name:'Ofunmeji',cost:1,type:'Ifa',desc:'Deal 4 damage.'},
      {name:'Osemeji',cost:1,type:'Ifa',desc:'Gain 3 Block.'}
    ],
    log:['Run begins at Floor 1: The Descent.'],
    over:false,
  };
}

function enemyIntent(){ return INTENTS[state.enemy.turn % INTENTS.length]; }

function render(){
  document.getElementById('hud').innerHTML = `<strong>Player</strong><br>HP ${state.player.hp}/${state.player.maxHp} | Àṣẹ ${state.player.ase} | Block ${state.player.block}`;
  document.getElementById('enemy').innerHTML = `<strong>Enemy</strong><br>${state.enemy.name} HP ${state.enemy.hp}/${state.enemy.maxHp} | Intent ${enemyIntent()} | Strength ${state.enemy.strength}`;

  const handEl = document.getElementById('hand');
  handEl.innerHTML = '<strong>Hand</strong><div class="hand-grid"></div>';
  const grid = handEl.querySelector('.hand-grid');
  state.hand.forEach((c, idx)=>{
    const div=document.createElement('div'); div.className='card';
    div.innerHTML=`<strong>${c.name}</strong><br><small>${c.type} • Cost ${c.cost}</small><p>${c.desc}</p>`;
    const btn=document.createElement('button'); btn.textContent='Play';
    btn.disabled=state.over || c.cost>state.player.ase;
    btn.onclick=()=>playCard(idx);
    div.appendChild(btn); grid.appendChild(div);
  });

  const msg = state.enemy.hp<=0 ? '<div><strong>Victory!</strong></div>' : state.player.hp<=0 ? '<div><strong>Defeat.</strong></div>' : '';
  document.getElementById('log').innerHTML = `<strong>Battle Log</strong>${msg}<ul>${state.log.slice(-10).map(l=>`<li>${l}</li>`).join('')}</ul>`;
}

function enemyTurn(){
  if(state.enemy.hp<=0 || state.player.hp<=0) return;
  const intent = enemyIntent();
  if(intent==='attack'){
    const dmg = 5 + state.enemy.strength;
    const taken = Math.max(0, dmg - state.player.block);
    state.player.block = Math.max(0, state.player.block - dmg);
    state.player.hp = Math.max(0, state.player.hp - taken);
    state.log.push(`Enemy attacks for ${dmg}; you take ${taken}.`);
  } else if(intent==='defend'){
    state.enemy.hp = Math.min(state.enemy.maxHp, state.enemy.hp + 3);
    state.log.push('Enemy fortifies and recovers 3 HP.');
  } else {
    state.enemy.strength += 1;
    state.log.push('Enemy gains +1 Strength.');
  }
  state.enemy.turn += 1;
}

function refreshTurnIfNeeded(){
  if(state.hand.length===0 && state.enemy.hp>0 && state.player.hp>0){
    state.player.ase=3; state.player.block=0;
    state.hand=[
      {name:'Strike (Ogun)',cost:1,type:'Attack',desc:'Deal 6 damage.'},
      {name:'Defend (Obatala)',cost:1,type:'Skill',desc:'Gain 5 Block.'},
      {name:'Ofunmeji',cost:1,type:'Ifa',desc:'Deal 4 damage.'}
    ];
    state.log.push('New turn: drew 3 cards and reset Àṣẹ to 3.');
  }
}

function playCard(index){
  const c = state.hand[index];
  if(!c || c.cost>state.player.ase || state.over) return;
  state.player.ase -= c.cost;
  state.log.push(`Played ${c.name}.`);
  if(c.name.startsWith('Strike')) state.enemy.hp=Math.max(0,state.enemy.hp-6);
  if(c.name==='Ofunmeji') state.enemy.hp=Math.max(0,state.enemy.hp-4);
  if(c.name.startsWith('Defend')) state.player.block+=5;
  if(c.name==='Osemeji') state.player.block+=3;
  state.hand.splice(index,1);

  if(state.enemy.hp>0) enemyTurn();
  if(state.enemy.hp<=0 || state.player.hp<=0) state.over=true;
  refreshTurnIfNeeded();
  render();
}

document.getElementById('newRun').addEventListener('click', ()=>{ state=initialState(); render(); });
state = initialState();
render();
