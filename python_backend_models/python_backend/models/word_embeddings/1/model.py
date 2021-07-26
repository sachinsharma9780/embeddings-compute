
# contains some utility functions for extracting information from model_config
# and converting Triton input/output types to numpy types.

import triton_python_backend_utils as pb_utils
import numpy as np
from sentence_transformers import SentenceTransformer

"""test_sent = ["Who are you voting for 2021?", "hi", "lol"]
model = SentenceTransformer('paraphrase-mpnet-base-v2')
sent_embed = model.encode(test_sent)"""
responses = []
sent_emb = []
class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to intialize any state associated with this model.
        Parameters
        ----------
        args : dict
          Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        self.model = SentenceTransformer('paraphrase-mpnet-base-v2')

    def run_model(self, inp):
        #inp = inp.as_numpy()[idx].decode("utf-8")
        inp = [v.decode("utf-8") for v in inp.as_numpy()]
        sentence_embeddings = self.model.encode(inp)

        #out_tensor_0 = pb_utils.Tensor("OUTPUT0",
        #                               np.array([sentence_embeddings], dtype=object))

        #inference_response = pb_utils.InferenceResponse(
        #    output_tensors=[out_tensor_0])
        #responses.append(inference_response)
        #sent_emb.append(sentence_embeddings)
        return sentence_embeddings

    def execute(self, requests):
        """`execute` must be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference is requested
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse.
        Parameters
        ----------
        requests : list
          A list of pb_utils.InferenceRequest
        Returns
        -------
        list
          A list of pb_utils.InferenceResponse. The length of this list must
          be the same as `requests`
        """

        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for idx, request in enumerate(requests):
            # Get INPUT0
            in_0 = pb_utils.get_input_tensor_by_name(request, "INPUT0")
            emb = self.run_model(in_0)
            #for index in range(2):
            #    emb = self.run_model(in_0, index)
            #in_0 = in_0.as_numpy()[idx].decode("utf-8")
            #sentence_embeddings = self.model.encode(in_0)
            # Create output tensors. You need pb_utils.Tensor
            # objects to create pb_utils.InferenceResponse.
            out_tensor_0 = pb_utils.Tensor("OUTPUT0",
                                           emb)

            # Create InferenceResponse.
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor_0])
            responses.append(inference_response)

        # You should return a list of pb_utils.InferenceResponse. Length
        # of this list must match the length of `requests` list.
        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is optional. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print('Cleaning up...')