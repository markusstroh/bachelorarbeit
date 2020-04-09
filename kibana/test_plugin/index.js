import { resolve } from 'path';
import { existsSync } from 'fs';

import { i18n } from '@kbn/i18n';

import exampleRoute from './server/routes/example'
import searchRoute from './server/routes/search_test'

export default function(kibana) {
  return new kibana.Plugin({
    id: "test_plugin",
    require: ['elasticsearch'],
    name: 'test_plugin',
    uiExports: {
      app: {
        title: 'Test Plugin',
        description: 'This is a test plugin',
        main: 'plugins/test_plugin/app',
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
      searchRoute(server);
      /*
      const xpackMainPlugin = server.plugins.xpack_main;
      if (xpackMainPlugin) {
        const featureId = 'test_plugin';

        xpackMainPlugin.registerFeature({

          id: featureId,
          name: i18n.translate('testPlugin.featureRegistry.featureName', {
            defaultMessage: 'test-plugin',
          }),
          navLinkId: featureId,
          icon: 'questionInCircle',
          app: [featureId, 'kibana'],
          catalogue: [],
          privileges: {
            all: {
              api: [],
              savedObject: {
                all: [],
                read: [],
              },
              ui: ['show'],
            },
            read: {
              api: [],
              savedObject: {
                all: [],
                read: [],
              },
              ui: ['show'],
            },
          },
        });
      }*/
    },
  });
}
