import { resolve } from 'path';
import { existsSync } from 'fs';

import { i18n } from '@kbn/i18n';

import exampleRoute from './server/routes/server'

export default function(kibana) {
  return new kibana.Plugin({
    id: "customer_analytics",
    require: ['elasticsearch'],
    name: 'Customer Analytics',
    uiExports: {
      app: {
        title: 'Customer Analytics',
        description: 'This plugin contains some methods for customer analytics',
        main: 'plugins/customer_analytics/app',
      },
      styleSheetPaths: [
        resolve(__dirname, 'public/app.scss'),
        resolve(__dirname, 'public/app.css'),
      ].find(p => existsSync(p)),
    },

    config(Joi) {
      return Joi.object({
        enabled: Joi.boolean().default(true),
      }).default();
    },

    // eslint-disable-next-line no-unused-vars
    init(server, options) {
      exampleRoute(server);
    },
  });
}
