import { Label } from 'src/components/label';
import { SvgColor } from 'src/components/svg-color';

// ----------------------------------------------------------------------

const icon = (name: string) => (
  <SvgColor width="100%" height="100%" src={`/assets/icons/navbar/${name}.svg`} />
);

export const navData = [
  {
    title: 'Статистика',
    path: '/',
    icon: icon('ic-analytics'),
  },
  {
    title: 'Таблицы',
    path: '/user',
    icon: icon('ic-user'),
  },
  {
    title: 'Вход',
    path: '/sign-in',
    icon: icon('ic-lock'),
  },
];
