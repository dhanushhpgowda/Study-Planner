document.addEventListener('DOMContentLoaded', () => {
  animateProgressBars();
  animateWeeklyBars();
  animateRing();
  animateStatCards();
});

function animateProgressBars() {
  const fills = document.querySelectorAll('.subj-prog-fill');
  fills.forEach((fill, i) => {
    const target = fill.style.width;
    fill.style.width = '0%';
    setTimeout(() => {
      fill.style.transition = 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
      fill.style.width = target;
    }, 100 + i * 100);
  });
}

function animateWeeklyBars() {
  const bars = document.querySelectorAll('.week-bar');
  const maxSessions = Math.max(
    ...Array.from(bars).map(b => parseInt(b.dataset.total) || 1), 1
  );

  bars.forEach((bar, i) => {
    const completed = parseInt(bar.dataset.completed) || 0;
    const total     = parseInt(bar.dataset.total) || 0;
    const targetH   = total > 0 ? Math.max((completed / maxSessions) * 120, 4) : 4;

    bar.style.height = '4px';
    bar.style.background = completed === 0
      ? 'rgba(255,255,255,0.08)'
      : completed === total
        ? '#4ade80'
        : '#f5a623';

    setTimeout(() => {
      bar.style.transition = 'height 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.height = targetH + 'px';
    }, 50 + i * 60);
  });
}

function animateRing() {
  const ring = document.querySelector('.ring-anim');
  if (!ring) return;
  const target = ring.getAttribute('stroke-dasharray');
  const total  = target.split(' ')[1];
  ring.setAttribute('stroke-dasharray', `0 ${total}`);
  setTimeout(() => {
    ring.style.transition = 'stroke-dasharray 1.2s cubic-bezier(0.4, 0, 0.2, 1)';
    ring.setAttribute('stroke-dasharray', target);
  }, 200);
}

function animateStatCards() {
  const cards = document.querySelectorAll('.stat-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 80 + i * 60);
  });
}