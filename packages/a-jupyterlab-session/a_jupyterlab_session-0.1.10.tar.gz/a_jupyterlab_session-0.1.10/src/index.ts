import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { URLExt } from '@jupyterlab/coreutils';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { ServerConnection } from '@jupyterlab/services';

/**
 * Initialization data for the a-jupyterlab-session extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'a-jupyterlab-session:plugin',
  autoStart: true,
  requires: [IDefaultFileBrowser],
  activate: async (
    app: JupyterFrontEnd,
    defaultFileBrowser: IDefaultFileBrowser
  ) => {
    const API_ENDPOINT = 'api/a-session';

    console.log('JupyterLab extension a-jupyterlab-session is activated!');

    const url = URLExt.join(
      app.serviceManager.serverSettings.baseUrl,
      API_ENDPOINT
    );
    const response = await ServerConnection.makeRequest(
      url,
      {},
      app.serviceManager.serverSettings
    );

    if (response.status !== 200) {
      const err = await ServerConnection.ResponseError.create(response);
      throw err;
    }

    const session = await response.text();

    await defaultFileBrowser.model.cd(session);
  }
};

export default plugin;
